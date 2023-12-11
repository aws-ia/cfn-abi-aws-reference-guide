'''
Delete all resources created during ABI module testing
'''
from time import sleep
from os.path import isfile
import json
import logging
import argparse

import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

SESSION = boto3.session.Session()
print(f"Region: {SESSION.region_name}")

CF = SESSION.client('cloudformation')
SSM = SESSION.client('ssm')
S3 = SESSION.client('s3')
STS = SESSION.client('sts')
ORG  = SESSION.client('organizations')
GD  = SESSION.client('guardduty')

STACKSTATUS = [ 'ROLLBACK_FAILED', 'ROLLBACK_COMPLETE', 'DELETE_FAILED', 'DELETE_COMPLETE']

def list_stacksets():
    '''List all stacksets in the account'''
    response = CF.list_stack_sets()
    stacksets = response['Summaries']
    while response.get('NextToken'):
        response = CF.list_stack_sets(NextToken=response['NextToken'])
        stacksets.extend(response['Summaries'])
    return stacksets

def list_active_stackset_names():
    '''List all stackset names in the account'''
    cf_names = []
    for cfn in list_stacksets():
        if cfn['Status'] != 'DELETED':
            cf_names += [cfn['StackSetName']]
    return cf_names

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

def get_ou_list(account_list):
    '''
    Return list of ous for provided list of accounts
    '''
    ou_list = []
    for account in account_list:
        ou_id = ORG.list_parents(ChildId=account)['Parents'][0]['Id']
        ou_list.append(ou_id)
    return list(set((ou_list)))

def delete_all_stackinstances(stackset_name):
    '''Delete a stackset'''
    response = None
    perm_model = CF.describe_stack_set(StackSetName=stackset_name)['StackSet']['PermissionModel']
    account_list = list(dict.fromkeys(si_account_list(stackset_name)))
    ou_list = get_ou_list(account_list)
    region_list = list(dict.fromkeys(si_region_list(stackset_name)))
    if len(account_list) != 0 and len(region_list) != 0:
        if perm_model == 'SERVICE_MANAGED':
            print(f"Deleting {stackset_name} in {region_list} with {ou_list}")
            response = CF.delete_stack_instances(StackSetName=stackset_name,
                        Regions=region_list, DeploymentTargets={'OrganizationalUnitIds': ou_list},
                        RetainStacks=False)
        else:
            print(f"Deleting {stackset_name} in {region_list} with {account_list}")
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
        sss_session = establish_remote_session(account)
        type(sss_session)
        sss = sss_session.resource('s3')
    else:
        sss = boto3.resource('s3')

    bucket = sss.Bucket(bucket_name)

    print('..Deleting all objects from bucket: %s', bucket_name)
    bucket.object_versions.delete()
    bucket.objects.all().delete()

def delete_s3_buckets(item):
    '''Delete all S3 buckets created by CfCT solution in the account'''

    filters=item['Filter']
    (sss, account, target) = get_client_session(item, 's3')

    print(f"S3 action on {target} with filters: {filters}")

    response = sss.list_buckets()
    buckets = response['Buckets']

    while response.get('NextToken'):
        response = sss.list_buckets(NextToken=response['NextToken'])
        buckets.extend(response['Buckets'])

    for bucket in buckets:
        bucket_name = bucket['Name']
        if bucket_name.startswith(filters):
            try:
                delete_all_objects_from_s3_bucket(bucket_name, account)
                print(f"....Deleting bucket: {bucket_name}")
                sss.delete_bucket(Bucket=bucket_name)
            except Exception as exe:
                if exe.response['Error']['Code'] == 'NoSuchBucket':
                    print(f"S3 bucket deletion issue. Skipping: {bucket_name}")
                else:
                    raise exe

def list_all_parameters(ssm_session=SSM):
    ''''List all parameters in the account'''
    response = ssm_session.describe_parameters()
    parameters = response['Parameters']
    while response.get('NextToken'):
        response = ssm_session.describe_parameters(NextToken=response['NextToken'])
        parameters.extend(response['Parameters'])
    return parameters

def delete_parameters(item):
    '''Delete all parameters created in the account'''

    filters = item['Filter']
    (ssm_session, account, target) = get_client_session(item, 'ssm')
    print(f"SSM action on {target} with filters: {filters}")

    parameters = list_all_parameters(ssm_session)
    for parameter in parameters:
        param_name = parameter['Name']
        if param_name.startswith(filters):
            print(f"..Deleting parameter {param_name}.")
            ssm_session.delete_parameter(Name=param_name)

def get_temp_credentials(aws_account, role_name='AWSControlTowerExecution'):
    '''
    Get temporary credentials from STS
    '''
    role_arn = 'arn:aws:iam::' + aws_account + ':role/' + role_name
    result = None
    try:
        response = STS.assume_role(
            RoleArn=role_arn,
            RoleSessionName=str(aws_account + '-' + role_name),
            DurationSeconds=3600
        )
        result = response['Credentials']
    except Exception as exe:
        if exe.response['Error']['Code'] == 'AccessDenied':
            print('Access denied to assume role: %s', role_arn)
        else:
            print('Error assuming role: %s', role_arn)

    return result

def establish_remote_session(account):
    '''
    Establish remote session
    '''

    roles = ['AWSControlTowerExecution', 'OrganizationAccountAccessRole']
    result = None

    for role in roles:
        sts_creds = get_temp_credentials(account, role)
        if sts_creds:
            result = boto3.Session(
            aws_access_key_id=sts_creds['AccessKeyId'],
            aws_secret_access_key=sts_creds['SecretAccessKey'],
            aws_session_token=sts_creds['SessionToken']
            )
            break

    return result

def get_log_archive_account(parameter_name='/sra/gd/control-tower/log-archive-account-id'):
    '''
    Get log archive account ID
    '''
    response = SSM.get_parameter(Name=parameter_name)
    return response['Parameter']['Value']

def get_list_of_accounts():
    '''
    Get list of accounts
    '''
    accounts = []
    paginator = ORG.get_paginator('list_accounts')
    for page in paginator.paginate():
        accounts += page['Accounts']
    return accounts

def get_account_id(filters='Log Archive'):
    '''
    Get log account ID
    '''
    acct_id = None
    for account in get_list_of_accounts():
        if account['Name'] == filters:
            acct_id  = account['Id']
    return acct_id

def list_cw_lognames(context):
    '''
    List all CloudWatch logs
    '''
    response = context.describe_log_groups()
    log_groups = response['logGroups']
    result = []
    while response.get('nextToken'):
        response = context.describe_log_groups(nextToken=response['nextToken'])
        log_groups.extend(response['logGroups'])

    for log in log_groups:
        result.append(log['logGroupName'])

    return result

def delete_cw_logs(item):
    '''
    Delete the pre-req data created during testing
    '''

    filters = item['Filter']
    (cw_session, account, target) = get_client_session(item, 'logs')
    print(f"LOG GROUP action on {target} with filters: {filters}")

    log_groups = list_cw_lognames(context=cw_session)
    for log_group_name in log_groups:
        if log_group_name.startswith(filters):
            print(f"..Deleting log group {log_group_name}.")
            cw_session.delete_log_group(logGroupName=log_group_name)

def get_management_account_id():
    '''
    Return management account ID
    '''
    return ORG.describe_organization()['Organization']['MasterAccountId']

def get_list_of_detectors(gd_client):
    '''
    Get list of GuardDuty detectors
    '''
    detectors = []
    paginator = gd_client.get_paginator('list_detectors')
    for page in paginator.paginate():
        detectors += page['DetectorIds']
    return detectors

def delete_detector():
    '''
    Delete the GuardDuty detectors in all accounts in the organization in the current region
    '''
    accounts = get_list_of_accounts()
    mgt_acct_id = get_management_account_id()

    for account in accounts:
        if mgt_acct_id != account['Id']:
            session = establish_remote_session(account['Id'])
            if session:
                gd_client = session.client('guardduty')
            else:
                print('Unable to establish session for account: %s', account['Id'])
                gd_client = None
        else: # Management account
            gd_client = boto3.client('guardduty')

        if gd_client:
            detector_ids = get_list_of_detectors(gd_client)
            for det_id in detector_ids:
                print('Deleting GuardDuty Detector in %s', account['Id'])
                gd_client.delete_detector(DetectorId=det_id)

def list_cb_projects():
    '''
    List all CodeBuild projects
    '''
    cb_session = SESSION.client('codebuild')
    response = cb_session.list_projects()
    projects = response['projects']
    while response.get('nextToken'):
        response = cb_session.list_projects(nextToken=response['nextToken'])
        projects.extend(response['projects'])

    return projects

def delete_build_projects(filters='sra-codebuild-'):
    '''
    Delete the CodeBuild projects in all accounts in the organization in the current region
    '''
    projects = list_cb_projects()
    for project in projects:
        if project.startswith(filters):
            print('Deleting CodeBuild project: %s', project)
            cb_session = SESSION.client('codebuild')
            cb_session.delete_project(name=project)

def get_account_info(ss_name='AWSControlTowerLoggingResources'):
    '''
    List first stack instances in a stackset
    '''
    result = None

    if ss_name in list_active_stackset_names():
        instance = CF.list_stack_instances(StackSetName=ss_name)
        account_id = instance['Summaries'][0]['Account']
        for account in get_list_of_accounts():
            if account['Id'] == account_id:
                account_name = account['Name']
        result = {'AccountName': account_name, 'AccountID': account_id}
    return result

def get_client_session(item, client_name):
    '''
    Return a session for parent or child
    '''

    account = None
    if 'Account' in item:
        if item['Account'] in ACCOUNTS:
            account = get_account_id(ACCOUNTS[item['Account']])
    if account:
        session = establish_remote_session(account)
        client_session = session.client(client_name)
        target = account
    else:
        client_session = boto3.client(client_name)
        target = STS.get_caller_identity()['Account']

    return (client_session, account, target)

def delete_iam_role(item):
    '''
    Delete an IAM role - complete role name must be provided
    '''

    role_name = item['Filter']
    (iam_session, account, target) = get_client_session(item, 'iam')
    print(f"IAM action on {target} with role_name: {role_name}")

    try:
        policies = iam_session.list_attached_role_policies(RoleName=role_name)
        for policy in policies['AttachedPolicies']:
            print(f"..Detaching policy {policy['PolicyArn']} from role {role_name}.")
            iam_session.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])
        print(f"....Deleting role {role_name}.")
        iam_session.delete_role(RoleName=role_name)
    except Exception as exe:
        if exe.response['Error']['Code'] == 'NoSuchEntity':
            print(f"IAM Role {role_name} does not exist.")
        else:
            raise exe

def run_cleanup(config):
    '''
    Run the cleanup
    '''
    for item in config:
        if item['Type'] == 'STACK':
            delete_stack(filters=item['Filter'])
        elif item['Type'] == 'S3_BUCKET':
            delete_s3_buckets(item)
        elif item['Type'] == 'SSM_PARAMETER':
            delete_parameters(item)
        elif item['Type'] == 'STACK_SET':
            delete_stacksets(filters=item['Filter'])
        elif item['Type'] == 'IAM_ROLE':
            delete_iam_role(item)
        elif item['Type'] == 'CODE_BUILD':
            delete_build_projects(filters=item['Filter'])
        elif item['Type'] == 'LOG_GROUP':
            delete_cw_logs(item)
        elif item['Type'] == 'GUARDDUTY_DET':
            delete_detector()
        else:
            print('Invalid type in cleanup_config.json: %s', item['Type'])


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(prog='cleanup_config.py',
                                     usage='%(prog)s [-C | -h]',
                                     description='Clear the configuration.')
    PARSER.add_argument("-C", "--config", default='cleanup_config.json',
                        help="Clear content from config")

    ARGS = PARSER.parse_args()

    LOG_ACCT_INFO = get_account_info('AWSControlTowerLoggingResources')
    AUDIT_ACCT_INFO = get_account_info('AWSControlTowerSecurityResources')
    if LOG_ACCT_INFO:
        LOG_ACCT_NAME = LOG_ACCT_INFO['AccountName']
    else:
        LOG_ACCT_NAME = 'Log Archive'

    if AUDIT_ACCT_INFO:
        AUDIT_ACCT_NAME = AUDIT_ACCT_INFO['AccountName']
    else:
        AUDIT_ACCT_NAME = 'Audit'

    ACCOUNTS = {"log_account": LOG_ACCT_NAME, "audit": AUDIT_ACCT_NAME}
    print('Recieved Account Info: %s', ACCOUNTS)
    CLEAR_CFG = ARGS.config

    if isfile(CLEAR_CFG):
        with open(CLEAR_CFG, encoding="utf-8") as json_file:
            CONFIG = json.load(json_file)
            run_cleanup(CONFIG)
    else:
        print('Config file not found: %s', CLEAR_CFG)
