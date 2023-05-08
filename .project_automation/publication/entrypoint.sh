#!/bin/bash -ex

## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype

cd ${PROJECT_PATH}/guide
hugo
aws s3 cp --recursive public s3://tcat-cfn-abi-aws-reference-guide-l1iqw9pj/docs-preview/ --acl public-read

echo "docs published here: s3://tcat-cfn-abi-aws-reference-guide-l1iqw9pj/docs-preview/"

# if [ -n "${BASE_PATH}" ]
# then
#   echo "Running Publication"
#   taskcat upload
# else
#   echo "Local build mode (skipping publication)"
# fi

