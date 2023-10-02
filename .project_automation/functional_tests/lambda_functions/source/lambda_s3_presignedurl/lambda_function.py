import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    # Specify the region when creating a session
    session = boto3.Session(region_name='us-east-1')
    # Create an S3 client
    s3 = session.client('s3')
    s3_file_with_key = event['s3_file_with_key']
    bucket_name = event['bucket_name']
    try:
            # Generate the URL to get 's3_file' from 'bucket'
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': s3_file_with_key
                },
                ExpiresIn=604800 #7 days expiration time 
            )
            logger.info(url)
            return {
                "Scoutsuite results can be downloaded from: ": f"{url}"
            }
    except ClientError as error:
            logger.exception (error)
            return {
                "error": "Failed to generate presigned URL",
                "details": str(error)
            }