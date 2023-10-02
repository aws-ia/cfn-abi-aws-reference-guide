import os
'''Used to walk through scoutsuite files in local filesystem and add the custom scoutsuite rules needed for ABI testing'''
import subprocess
'''Used to check scoutsuite path in local filesystem in order to copy the custom scoutsuite rules needed for ABI testing'''
import logging
import shutil
import sys

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)

def copy_file(src, dst):
    '''Function that copies a file from a source directory to a destination directory'''
    if not os.path.exists(dst):
        try:
            shutil.copy(src, dst)
            logging.info(f"File {src} copied successfully to Scoutsuite aws custom findings directory.")
        except shutil.Error as error:
            logging.info(f"Error: {error}")
        except IOError as error:
            logging.info(f"Error: {error.strerror}")
    else:
        logging.info(f"Error: The destination file {dst} already exists.")


def create_scoutsuite_custom_rule_file(file_name):
    '''Function that retrieves the Scoutsuite directory in the current execution environment'''
    result = subprocess.run(['pip', 'show', 'scoutsuite'], capture_output=True, text=True)
    scout_path = None
    for line in result.stdout.split('\n'):
        if line.startswith('Location:'):
            scout_path = line.split(': ')[1]
    if scout_path is None:
        logging.warning("ScoutSuite is not installed or could not find the installation path.")
        sys.exit(1)

    # Scoutsuite aws cloudtrail custom rule finding json
    scoutsuite_cloudtrail_json_file_path = os.path.join(scout_path, 'ScoutSuite', 'providers', 'aws', 'rules', 'findings', file_name)

    # Check if the file exists
    if not os.path.exists(scoutsuite_cloudtrail_json_file_path):
        # If the file does not exist, create it   
        # Source path
        src = '.project_automation/functional_tests/'+file_name
        copy_file(src, scoutsuite_cloudtrail_json_file_path)
    else:
        logging.info(f'File {scoutsuite_cloudtrail_json_file_path} already exists')

def main():
    custom_rules = ['abi-iam-assume-role-lacks-external-id-and-mfa.json', 'abi-cloudtrail-no-encryption-with-kms.json']
    for rule in custom_rules:
        create_scoutsuite_custom_rule_file(rule)

if __name__ == "__main__":
    main()