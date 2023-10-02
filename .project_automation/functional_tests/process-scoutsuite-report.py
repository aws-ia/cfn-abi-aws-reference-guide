import os
import fnmatch
import json
import boto3
import zipfile
import datetime
import logging
from botocore.exceptions import ClientError
from io import BytesIO
import time

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)

# Specify the region when creating a session
session = boto3.Session(region_name='us-east-1')
# Create an STS client        
sts = session.client('sts')

# Call the 'get_caller_identity' function
response = sts.get_caller_identity()

# Extract the account ID
account_id = response['Account']

def current_time_key():
    '''Get the current time and format it into a string'''
    now = datetime.datetime.now()
    return now.strftime("%Y%m%d%H%M%S")

def find_js_files(directory, prefix):
    '''Function to find js file in a specific directory'''
    matches = []
    for root, _dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, f'{prefix}*.js'):
            matches.append(os.path.join(root, filename))
    return matches

def zip_folder(folder_path, zip_name):
    '''Function used to zip all files from scoutsuite-report folder'''
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Keeps folder structure in the archive
                zipf.write(file_path, arcname)

def get_scoutsuite_results():
    '''Function to retrieve scoutsuite results from the scoutsuite results js file'''
    directory_path = './scoutsuite-report/scoutsuite-results/'
    file_prefix = 'scoutsuite_results_aws'
    matches = find_js_files(directory_path, file_prefix)

    for match in matches:
        with open(match) as f:
            json_payload = f.readlines()
            json_payload.pop(0)
            json_payload = ''.join(json_payload)
            json_file = json.loads(json_payload)
            return(json_file)

def zip_folder_to_bytesio(folder_path):
    """
    Function that zips the contents of an entire folder and return a BytesIO object containing the zipped data.
    """
    parent_folder = os.path.dirname(folder_path)
    contents = os.walk(folder_path)
    
    zip_data = BytesIO()
    
    with zipfile.ZipFile(zip_data, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in contents:
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                zipf.write(absolute_path, file_name)

    # Important: move the BytesIO object's position to the beginning
    zip_data.seek(0)
    return zip_data

def create_lambda_s3_presignedurl():
    '''Function that creates the Lambda function that generates S3 presigned URLs'''

    # Create the ZIP deployment package for Lambda
    lambda_zipped_code = zip_folder_to_bytesio('./.project_automation/functional_tests/lambda_functions/source/lambda_s3_presignedurl')
    lambda_zipped_code.seek(0) # Reset the cursor of the BytesIO object to the beginning

    s3_client = session.client('s3')
    bucket_name = 'scoutsuite-results-aws-' + account_id
    object_name = 'lambda_s3_presignedurl/package/lambda_function.zip'  # the key under which the file should be stored

    s3_client.upload_fileobj(lambda_zipped_code, bucket_name, object_name)

    stack_name = "Lambda-S3-PresignedURL"

    # Use the session to create a client for CloudFormation
    cf_client = session.client('cloudformation')

    with open('./.project_automation/functional_tests/lambda_s3_presignedurl.yaml', 'r') as file:
        template_body = file.read()
    # Check if the stack already exists
    try:
        cf_client.describe_stacks(StackName=stack_name)
        # If the above did not raise an exception, it means the stack exists. So we update it.
        cf_client.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND']
        )

        waiter = cf_client.get_waiter('stack_update_complete')
        waiter.wait(StackName=stack_name)
        logging.info(f"Stack {stack_name} update is complete.")
    except cf_client.exceptions.ClientError as error:
        error_message = str(error)
        if error_message != 'An error occurred (ValidationError) when calling the UpdateStack operation: No updates are to be performed.':
            # If the stack does not exist, we create it.
            cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Capabilities=['CAPABILITY_NAMED_IAM', 'CAPABILITY_AUTO_EXPAND']
            )
            waiter = cf_client.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
            logging.info(waiter.name)
            logging.info(f"Stack {stack_name} deployment is complete.")
            


def get_lambda_state(function_name):
    lambda_client = session.client('lambda')
    
    try:
        response = lambda_client.get_function(FunctionName=function_name)
        return response['Configuration']['State']
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

def wait_until_lambda_active(function_name, max_retries=10, delay=10):
    """
    Wait until the Lambda function is Active.
    
    Parameters:
    - function_name: Name of the Lambda function.
    - max_retries: Maximum number of retry attempts.
    - delay: Delay (in seconds) between retry attempts.
    """
    retries = 0
    while retries < max_retries:
        state = get_lambda_state(function_name)
        if state == 'Active':
            print(f"The function {function_name} is now {state}")
            return True
        else:
            print(f"Function {function_name} is in state {state}. Retrying in {delay} seconds...")
            time.sleep(delay)
            retries += 1

    print(f"Function {function_name} did not become Active after {max_retries} retries.")
    return False

def generate_s3_presignedurl(bucket_name, s3_file_with_key):
    '''Invoke the Lambda Function that generates S3 presigned URLs'''
    # Initialize the boto3 client for Lambda
    lambda_client = session.client('lambda')

    # Specify the name of the Lambda function you want to invoke
    function_name = 'GenerateS3PresignedURLFunction'

    # S3 Bucket name and S3 object for the S3 presigned URL Lambda Function
    s3_object_details = {
        "s3_file_with_key":  s3_file_with_key,
        "bucket_name":  bucket_name
    }

    # Convert the file content to JSON string to send it as input
    input_payload = json.dumps(s3_object_details)

    #wait_until_lambda_active(function_name)

    try:
    # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # This specifies synchronous execution
            Payload=input_payload.encode('utf-8')
        )

        # Check if the Lambda invocation itself had an error (e.g., runtime errors in the Lambda function).
        if 'FunctionError' in response:
            raise Exception(f"Lambda function error: {response['FunctionError']} - {response['Payload'].read().decode('utf-8')}")

         # Read the Lambda function result
        response_payload = response['Payload'].read()
        if not response_payload:
            payload = None
        else:
            payload = json.loads(response_payload)
            logging.info(payload)

    except boto3.exceptions.Boto3Error as error:
        logging.exception(f"An error occurred while invoking the Lambda function: {error}")
    except json.JSONDecodeError:
        logging.error("Failed to decode the Lambda function's result as JSON.")
    except Exception as error:
        logging.error(f"An unexpected error occurred: {error}")

def upload_scoutsuite_results_zip_to_s3(scoutsuite_zip_file_path, zip_name):
    '''Function to retrieve scoutsuite results from the scoutsuite results zip file to an S3 private bucket with encryption and versioning enabled'''
    # Define the bucket name
    bucket_name = 'scoutsuite-results-aws-' + account_id

    s3 = session.client('s3')

    # Check if the bucket already exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as error:
        error_code = int(error.response['Error']['Code'])
        if error_code == 404:
            # If bucket does not exist, then create it
            s3.create_bucket(
                ACL='private',
                Bucket=bucket_name
            )

            # Enable versioning
            s3.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={
                    'MFADelete': 'Disabled',
                    'Status': 'Enabled'
                }
            )

            # Enable server side encryption
            s3.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'AES256'
                            }
                        },
                    ]
                }
            )
            # Apply a bucket policy to enforce HTTPS
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowSSLRequestsOnly",
                        "Effect": "Deny",
                        "Principal": "*",
                        "Action": "s3:*",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*",
                        "Condition": {
                            "Bool": {
                                "aws:SecureTransport": "false"
                            }
                        }
                    }
                ]
            }

            bucket_policy = json.dumps(bucket_policy)

            s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        else:
            logging.info("Unexpected error: %s" % error)

    try:
        # Generate a time-based key and add to the filename
        time_key = current_time_key()
        s3_file_with_key = time_key + '-' + zip_name
        # Upload the Scoutsuite results zip to an S3 bucket
        s3.upload_file(scoutsuite_zip_file_path, bucket_name, s3_file_with_key)

    except ClientError as error:
        logging.exception (error)

    create_lambda_s3_presignedurl()
    generate_s3_presignedurl(bucket_name, s3_file_with_key)

def check_scoutsuite_results(scout_suite_results):
    '''Function to retrieve Scoutsuite results and logs warning and danger levels found'''
    exit_counter = 0
    for service, info in scout_suite_results['last_run']['summary'].items():
        if info['max_level'] == 'warning':
            logging.info(f'Warning level in Scoutsuite security scan report found in service: {service}')

    for service, info in scout_suite_results['last_run']['summary'].items():
        if info['max_level'] == 'danger':
            logging.info(f'Danger level in Scoutsuite security scan report found in service: {service}')
            exit_counter=1
    
    if exit_counter == 0:
        logging.info('No Danger level in Scoutsuite security scan report found')
        # Write the Scoutsuite sysout result to a file
        with open("scoutsuite_sysout.txt", "w") as file:
            file.write(str(0))     
    else:
        # Write the Scoutsuite sysout result to a file
        with open("scoutsuite_sysout.txt", "w") as file:
            file.write(str(1))

def main():
    scoutsuite_results = get_scoutsuite_results()
    scoutsuite_results_folder_path = './scoutsuite-report/'
    zip_name = 'scoutsuite-report.zip' 
    zip_folder(scoutsuite_results_folder_path, zip_name)
    scoutsuite_zip_file_path = './' + zip_name
    upload_scoutsuite_results_zip_to_s3(scoutsuite_zip_file_path, zip_name)
    check_scoutsuite_results(scoutsuite_results)

if __name__ == "__main__":
    main()
