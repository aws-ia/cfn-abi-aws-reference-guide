'''
Delete all resources created during ABI module testing
'''
from time import sleep
import json
import logging
import argparse

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SESSION = boto3.session.Session()
print('Region: %s', SESSION.region_name)

CF = SESSION.client('cloudformation')
SSM = SESSION.client('ssm')
S3 = SESSION.client('s3')
STS = SESSION.client('sts')

STACKSTATUS = [ 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_FAILED', 'DELETE_COMPLETE']

def list_stacksets():
    '''List all stacksets in the account'''
    response = CF.list_stack_sets()
    stacksets = response['Summaries']
    while response.get('NextToken'):
        response = CF.list_stack_sets(NextToken=response['NextToken'])
        stacksets.extend(response['Summaries'])
    return stacksets

def list_stackset_names(filters=None):
    '''List all stackset names in the account'''
    cf_info = list_stacksets()
    cf_names = []
    for cfn in cf_info:
        if cfn['Status'] != 'DELETED':
            ss_name = cfn['StackSetName']
            if filters:
                if ss_name.startswith(filters):
                    cf_names += [ss_name]
            else:
                cf_names += [ss_name]

    return cf_names

def list_stackset_instances(stackset_name):
    '''List all stackset instances in the account'''
    response = CF.list_stack_instances(StackSetName=stackset_name)
    stackinstances = response['Summaries']
    while response.get('NextToken'):
        response = CF.list_stack_instances(StackSetName=stackset_name,
                                        NextToken=response['NextToken'])
        stackinstances.extend(response['Summaries'])
    return stackinstances

def delete_stack_instances(stackset_name, retain_stacks=False):
    '''Delete all stackset instances in the account'''
    stackinstances = list_stackset_instances(stackset_name)
    for stackinstance in stackinstances:
        CF.delete_stack_instances(StackSetName=stackset_name,
                                Regions=[stackinstance['Region']],
                                RetainStacks=retain_stacks)

def si_account_list(stackset_name):
    '''List all stackset instance accounts'''
    stackinstances = list_stackset_instances(stackset_name)
    stackinstance_names = []
    for stackinstance in stackinstances:
        stackinstance_names += [stackinstance['Account']]
    return stackinstance_names

def si_region_list(stackset_name):
    '''List all stackset instance regions'''
    stackinstances = list_stackset_instances(stackset_name)
    stackinstance_regions = []
    for stackinstance in stackinstances:
        stackinstance_regions += [stackinstance['Region']]
    return stackinstance_regions

def delete_all_stackinstances(stackset_name):
    '''Delete a stackset'''
    response = None
    account_list = list(dict.fromkeys(si_account_list(stackset_name)))
    region_list = list(dict.fromkeys(si_region_list(stackset_name)))
    if len(account_list) != 0 and len(region_list) != 0:
        response = CF.delete_stack_instances(StackSetName=stackset_name,
                            Regions=region_list,
                            Accounts=account_list,
                            RetainStacks=False)
        loop = 1
        while len(list_stackset_instances(stackset_name)) > 0 and loop < 30:
            sleep(10)
            loop += 1

    return response

def delete_stacksets(filters):
    '''Delete all stacksets created by CfCT solution in the account'''
    cf_names = list_stackset_names(filters)
    for cf_name in cf_names:
        op_info = delete_all_stackinstances(cf_name)
        op_id = op_info['OperationId']
        result = CF.describe_stack_set_operation(StackSetName=cf_name,
                                                    OperationId=op_id)
        op_status = result['StackSetOperation']['Status']
        while op_status != 'SUCCEEDED':
            sleep(10)
            result = CF.describe_stack_set_operation(StackSetName=cf_name,
                                                        OperationId=op_id)
            op_status = result['StackSetOperation']['Status']

        CF.delete_stack_set(StackSetName=cf_name)

def list_all_stacks():
    '''List all stacks in the account'''
    response = CF.list_stacks()
    stacks = response['StackSummaries']
    while response.get('NextToken'):
        response = CF.list_stacks(NextToken=response['NextToken'])
        stacks.extend(response['StackSummaries'])
    return stacks

def list_stack_status_by_name(stack_name):
    '''List stack status by stack name'''
    stacks = list_all_stacks()
    output = None
    for stack in stacks:
        if stack['StackName'] == stack_name:
            output = stack['StackStatus']
    return output

def is_nested_stack(stack_name):
    '''Check if stack is a nested stack'''
    stack = CF.describe_stacks(StackName=stack_name)['Stacks'][0]
    result = False
    if 'ParentId' in stack:
        result = True
    return result

def delete_stack(filters='tCaT-'):
    '''Delete all stacks created by CfCT solution in the account'''
    stacks = list_all_stacks()
    for stack in stacks:
        stack_name = stack['StackName']
        stack_status = stack['StackStatus']
        if stack_name.startswith(filters) and stack_status != 'DELETE_COMPLETE':
            if not is_nested_stack(stack_name):
                print('Deleting stack: %s', stack_name)
                CF.delete_stack(StackName=stack_name)
                wait = 1
                while list_stack_status_by_name(stack_name) not in STACKSTATUS and wait < 60:
                    print('Wait: %s, Stack: %s', stack_name, wait)
                    sleep(10)
                    wait += 1

def delete_all_objects_from_s3_bucket(bucket_name, account=None):
    '''Delete all objects from an S3 bucket'''
    if account:
        session = establish_remote_session(account)
        sss = session.resource('s3')
    else:
        sss = boto3.resource('s3')

    bucket = sss.Bucket(bucket_name)

    print('Deleting all objects from bucket: %s', bucket_name)
    bucket.object_versions.delete()
    bucket.objects.all().delete()

def delete_s3_buckets(filters='sra-staging-', account=None):
    '''Delete all S3 buckets created by CfCT solution in the account'''
    if account:
        session = establish_remote_session(account)
        sss = session.client('s3')
    else:
        sss = boto3.client('s3')

    response = sss.list_buckets()
    buckets = response['Buckets']
    while response.get('NextToken'):
        response = sss.list_buckets(NextToken=response['NextToken'])
        buckets.extend(response['Buckets'])
        print(buckets)
    for bucket in buckets:
        if bucket['Name'].startswith(filters):
            print(filters)
            try:
                delete_all_objects_from_s3_bucket(bucket['Name'], account)
                print('Deleting bucket: %s', bucket['Name'])
                sss.delete_bucket(Bucket=bucket['Name'])
            except Exception as exe:
                if exe.response['Error']['Code'] == 'NoSuchBucket':
                    print('S3 bucket deletion issue. Skipping: %s', bucket['Name'])
                else:
                    raise exe

def list_all_parameters():
    ''''List all parameters in the account'''
    response = SSM.describe_parameters()
    parameters = response['Parameters']
    while response.get('NextToken'):
        response = SSM.describe_parameters(NextToken=response['NextToken'])
        parameters.extend(response['Parameters'])
    return parameters

def delete_parameters(filters='/sra/'):
    '''Delete all parameters created by CfCT solution in the account'''
    parameters = list_all_parameters()
    for parameter in parameters:
        if parameter['Name'].startswith(filters):
            SSM.delete_parameter(Name=parameter['Name'])

def get_temp_credentials(aws_account, role_name='AWSControlTowerExecution'):
    '''
    Get temporary credentials from STS
    '''
    role_arn = 'arn:aws:iam::' + aws_account + ':role/' + role_name
    response = STS.assume_role(
        RoleArn=role_arn,
        RoleSessionName=str(aws_account + '-' + role_name),
        DurationSeconds=3600
    )
    return response['Credentials']

def establish_remote_session(account):
    '''
    Establish remote session
    '''

    sts_creds = get_temp_credentials(account)
    return boto3.Session(
        aws_access_key_id=sts_creds['AccessKeyId'],
        aws_secret_access_key=sts_creds['SecretAccessKey'],
        aws_session_token=sts_creds['SessionToken']
    )

def get_log_archive_account(parameter_name='/sra/gd/control-tower/log-archive-account-id'):
    '''
    Get log archive account ID
    '''
    response = SSM.get_parameter(Name=parameter_name)
    return response['Parameter']['Value']

def get_account_id(filters='Log Archive'):
    '''
    Get log account ID
    '''
    acct_id = None
    org = boto3.client('organizations')
    accounts = org.list_accounts()['Accounts']
    for account in accounts:
        if account['Name'] == filters:
            acct_id  = account['Id']
    return acct_id

def list_cw_lognames():
    '''
    List all CloudWatch logs
    '''
    cwlogs = SESSION.client('logs')
    response = cwlogs.describe_log_groups()
    log_groups = response['logGroups']
    result = []
    while response.get('nextToken'):
        response = cwlogs.describe_log_groups(nextToken=response['nextToken'])
        log_groups.extend(response['logGroups'])

    for log in log_groups:
        result.append(log['logGroupName'])

    return result

def delete_cw_logs(filters='sra/sra-org-trail'):
    '''
    Delete the pre-req data created during testing
    '''
    cwlogs = SESSION.client('logs')
    log_groups = list_cw_lognames()
    for log_group_name in log_groups:
        if log_group_name.startswith(filters):
            print('Deleting log group: %s', log_group_name)
            cwlogs.delete_log_group(logGroupName=log_group_name)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(prog='cleanup_config.py',
                                     usage='%(prog)s [-C | -h]',
                                     description='Clear the configuration.')
    PARSER.add_argument("-C", "--config", default='cleanup_config.json',
                        help="Clear content from config")

    ACCOUNTS = {"log_account": "Log Archive", "audit": "Audit"}
    ARGS = PARSER.parse_args()

    CLEAR_CFG = ARGS.config

    with open(CLEAR_CFG, encoding="utf-8") as json_file:
        CONFIG = json.load(json_file)
        for item in CONFIG:
            if item['Type'] == 'STACK':
                delete_stack(filters=item['Filter'])
            elif item['Type'] == 'S3_BUCKET':
                ACCOUNT_ID = None
                if 'Account' in item:
                    if item['Account'] in ACCOUNTS:
                        ACCOUNT_ID = get_account_id(ACCOUNTS[item['Account']])
                print('Account-id: %s', ACCOUNT_ID)
                delete_s3_buckets(filters=item['Filter'], account=ACCOUNT_ID)
            elif item['Type'] == 'SSM_PARAMETER':
                delete_parameters(filters=item['Filter'])
            elif item['Type'] == 'STACK_SET':
                delete_stacksets(filters=item['Filter'])
            elif item['Type'] == 'LOG_GROUP':
                delete_cw_logs(filters=item['Filter'])
            else:
                print('Invalid type in cleanup_config.json: %s', item['Type'])
