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
# Run taskcat e2e test without deleting resources
taskcat test run -n
#Create Scoutsuite security scan custom rule
python3 .project_automation/functional_tests/create-scoutsuite-custom-rule.py
# Execute Scoutsuite security scan
scout aws -r us-east-1 --ruleset .project_automation/functional_tests/abi-scoutsuite-custom-ruleset.json --no-browser --max-rate 5 --max-workers 5
# Upload Scoutsuite security scan results to S3 bucket named scoutsuite-results-aws-AWS-ACCOUNT-ID
python3 .project_automation/functional_tests/process-scoutsuite-report.py
# Delete taskcat e2e test resources
taskcat test clean ALL
# Check Scoutsuite security scan result for Danger level findings (Non-0 exit code)
scoutsuite_sysout_result=$(cat scoutsuite_sysout.txt)
rm scoutsuite_sysout.txt
if [ "$scoutsuite_sysout_result" -ne 0 ]; then
    # The value is non-zero, indicating Scoutsuite report needs to be checked for security issues
    exit 1 
fi

#sleep 1800 
#Use the command above to allow for a sleep timer buffer between sequential execution of Taskcat so that the Cloudformation resources from the previous Taskcat execution can be fully deleted until this is fixed in https://github.com/aws-ia/taskcat/issues/809

## Executing ash tool

#find ${PROJECT_PATH} -name lambda.zip -exec rm -rf {} \;

#git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

# Set the repo path in your shell for easier access
#export PATH=$PATH:/tmp/ash

#ash --source-dir .
#cat aggregated_results.txt

