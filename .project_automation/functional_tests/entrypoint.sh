#!/bin/bash -ex

## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype

cd ${PROJECT_PATH}

# Run taskcat e2e test
taskcat test run


#export AWS_DEFAULT_REGION=us-east-1
#ls -l ${PROJECT_PATH}/scripts/cleanup_config.py
#ls -l ${PROJECT_PATH}/scripts/cleanup_config.json 
#python3 scripts/cleanup_config.py -C scripts/cleanup_config.json
## Executing ash tool

#find ${PROJECT_PATH} -name lambda.zip -exec rm -rf {} \;

#git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

# Set the repo path in your shell for easier access
#export PATH=$PATH:/tmp/ash

#ash --source-dir .
#cat aggregated_results.txt

