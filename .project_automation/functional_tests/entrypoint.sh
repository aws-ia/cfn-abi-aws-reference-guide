#!/bin/bash -ex


## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype
NON_CT_ENV="039084729647"

cd ${PROJECT_PATH}

cleanup_region() {
    echo "Cleanup running in region: $1"
    export AWS_DEFAULT_REGION=$1
    python3 scripts/cleanup_config.py -C scripts/cleanup_config.json
}

cleanup_all_regions() {
    export AWS_DEFAULT_REGION=us-east-1
    regions=($(aws ec2 describe-regions --query "Regions[*].RegionName" --output text))
    for region in ${regions[@]}
    do
        cleanup_region ${region}
    done
}

run_test() {
    echo "Running e2e test: $1"
    cleanup_all_regions
    echo $AWS_DEFAULT_REGION
    unset AWS_DEFAULT_REGION
    echo $AWS_DEFAULT_REGION
    taskcat test run -n -t $1
    .project_automation/functional_tests/scoutsuite/scoutsuite.sh
}

acct_id=$(aws sts get-caller-identity --output text --query 'Account')

# if account id is xxxx do this
# if [ "$acct_id" == ${NON_CT_ENV} ]; then
#     run_test "launch-partner-solution-nonct"
# else
#    run_test "launch-partner-solution"
# fi
# Run taskcat e2e test
#run_test "launch-partner-solution"

#run_test "launch-partner-solution-nonct"

## Executing ash tool

#find ${PROJECT_PATH} -name lambda.zip -exec rm -rf {} \;

echo "Downloading the ASH tool"
git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

# Set the repo path in your shell for easier access
export PATH=$PATH:/tmp/ash

echo "Executing the ASH tool"
ash --source-dir .
pwd
ls -lrt

cat ${PROJECT_PATH}/ash_output/aggregated_results.txt
#cat aggregated_results.txt

