#!/bin/bash -ex


## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype

cd ${PROJECT_PATH}

regions=(us-east-1 us-east-2 us-west-2 us-west-1)
for region in ${regions[@]}
do
    echo "Cleanup running in region: $region"
    export AWS_DEFAULT_REGION=$region
    python3 scripts/cleanup_config.py -C scripts/cleanup_config.json
done

echo $AWS_DEFAULT_REGION
unset AWS_DEFAULT_REGION

echo $AWS_DEFAULT_REGION
# Run taskcat e2e test
taskcat test run

## Executing ash tool

#find ${PROJECT_PATH} -name lambda.zip -exec rm -rf {} \;

#git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

# Set the repo path in your shell for easier access
#export PATH=$PATH:/tmp/ash

#ash --source-dir .
#cat aggregated_results.txt

