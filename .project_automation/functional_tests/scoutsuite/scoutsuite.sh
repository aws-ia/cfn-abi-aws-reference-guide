#!/bin/bash -ex


## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype

cd ${PROJECT_PATH}

# Retrieve the AWS account ID and store it in a variable
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)

run_scoutsuite() {
    #Create Scoutsuite security scan custom rule
    python3 .project_automation/functional_tests/scoutsuite/create-scoutsuite-custom-rule.py
    # Execute Scoutsuite security scan
    scout aws -r us-east-1 --ruleset .project_automation/functional_tests/scoutsuite/abi-scoutsuite-custom-ruleset.json --no-browser --max-rate 5 --max-workers 5 -f
    # Upload Scoutsuite security scan results to S3 bucket named scoutsuite-results-aws-AWS-ACCOUNT-ID
    python3 .project_automation/functional_tests/scoutsuite/process-scoutsuite-report.py
    # Delete taskcat e2e test resources
    taskcat test clean ALL
    process_scoutsuite_report
}

process_scoutsuite_report() {
    # Check Scoutsuite security scan result for Danger level findings (Non-0 exit code)
    scoutsuite_sysout_result=$(cat scoutsuite_sysout.txt)
    scoutsuite_s3_filename=$(cat scoutsuite_s3_filename.txt)
    rm scoutsuite_sysout.txt
    rm scoutsuite_s3_filename.txt
    if [ "$scoutsuite_sysout_result" -ne 0 ]; then       
        # The value is non-zero, indicating Scoutsuite report needs to be checked for security issues
        echo "Scoutsuite report contains security issues. For details please check the log messages above or the file $scoutsuite_s3_filename in the S3 bucket named scoutsuite-results-aws-$AWS_ACCOUNT_ID in the AWS test account provided by the ABI team."
        exit 1 
    fi
}

#Run Scoutsuite security test
run_scoutsuite