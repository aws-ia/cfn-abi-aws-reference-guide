#!/bin/bash -ex

## NOTE: paths may differ when running in a managed task. To ensure behavior is consistent between
# managed and local tasks always use these variables for the project and project type path
PROJECT_PATH=${BASE_PATH}/project
PROJECT_TYPE_PATH=${BASE_PATH}/projecttype

echo "[STAGE: Publication]"
VERSION=$(cat VERSION)
echo $VERSION
BRANCH=main
EXISTING_GIT_VERSION="$(git tag -l)"
HUGO_VERSION=$(hugo version)
PUBLIC_PATH=./public
# ABP clones with HTTPS URL remotes
REPO_NAME=$(git config --get remote.origin.url | cut -d '/' -f5 | cut -d '.' -f1)
VERSION=$(cat VERSION)

BASE_URL="this would be the path to s3 bucket/${REPO_NAME}/"
S3_URI="s3://aws-abi/guide/${REPO_NAME}/"

if [[ $(echo $EXISTING_GIT_VERSION | grep $VERSION) ]]
then
  echo "version exists skipping release creation hint: Bump version in VERSION file"
else
  echo "creating new version"
  gh release create ${VERSION} --target ${BRANCH} --generate-notes
fi

print_header() {
  printf "\n\n%s\n" "$*"
}

sed -i 's/href=.*$/href="#">/' ${PROJECT_PATH}/guide/layouts/partials/logo.html

print_header 'Building site...'
cd ${PROJECT_PATH}/guide
hugo --verbose --debug

print_header 'Publishing...'
aws s3 sync --delete "${PUBLIC_PATH}" "${S3_URI}" --acl public-read

print_header 'Listing uploaded content...'
aws s3 ls --recursive --human-readable --summarize "${S3_URI}"

printf "\nPublished at ${BASE_URL}\n"

# Publish code to S3 bucket

cd ${PROJECT_PATH}

taskcat upload --bucket-name aws-abi --object-acl public-read

# if [ -n "${BASE_PATH}" ]
# then
#   echo "Running Publication"
#   taskcat upload
# else
#   echo "Local build mode (skipping publication)"
# fi

