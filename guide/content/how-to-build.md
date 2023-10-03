---
weight: 6
title: How to build an ABI project
description: Steps to create an ABI project
---

The below example refers to steps followed to create the sample ABI project in this repository. While building your project, update the steps below as per your project needs.

1. Once you have access to the repository, [fork the repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo?platform=linux#forking-a-repository). Example below to create a fork from CLI.

    ```
    gh auth login
    gh repo fork https://github.com/aws-ia/cfn-abi-aws-reference-guide.git
    ```

2. Add the **required** ABI Modules as submodules to your repository (The securityhub repo is used as a submodule in the below example.). 
    ```
    mkdir submodules
    cd submodules
    git submodule add https://github.com/aws-ia/cfn-abi-aws-securityhub.git
    ```
    Check here for [List of available ABI Modules](/available_modules/index.html).

3. Build and update the code as per your project needs. Follow the structure explained in the [Project Structure](/project-structure/index.html) section to organize your code. Below is an example of the directory structure for the sample ABI project in this repository:

    ```bash
    .
    ├── CODEOWNERS
    ├── CODE_OF_CONDUCT.md
    ├── LICENSE
    ├── NOTICE.txt
    ├── README.md
    ├── VERSION
    ├── guide
    │   ├── assets
    │   ├── config
    │   ├── content
    │   │   ├── _index.md
    │   │   │   ...
    │   │   │   ...
    │   │   └── overview.md
    │   │   ...
    │   ├── resources
    │   └── static
    ├── images
    │   └── abi-architecture.png
    ├── lambda_functions
    │   └── source
    │       └── enable_integrations
    │           ├── cfnresponse.py
    │           ├── copy_zips.py
    │           ├── enable_integration.py
    │           └── requirements.txt
    ├── scripts
    │   ├── cleanup_config.json
    │   └── cleanup_config.py
    ├── submodules
    │   └── cfn-abi-aws-securityhub
    │       ├── lambda_functions
    │       │   └── source
    │       ├── scripts
    │       └── templates
    └── templates
        ├── abi-enable-partner1-securityhub-integration.yaml
        └── enable_integrations
            └── partner1-enable-integrations.yaml

    83 directories, 394 files
    ```

    | **Note:** There is no need to package your lambda source. Taskcat will take care of it and upload it in the path of `lambda_functions/packages/<directory-name/lambda.zip>`. Please make references to your code as needed.|
    | --- |

4. Run static tests locally.

    Execute the following tests locally  in your environment, the same set of tests are executed as part of the pipeline validations done with these tests:

    * **cfn-lint tests:**

    ```
    pip3 install cfn-lint
    ```

    * **taskcat lint:**

    ```
    pip3 install taskcat
    ```

    * **cfn-nag tests and add exceptions if needed**
    Refer to instruction in the cfn-nag documentation to [apply per-resource rule suppression](https://github.com/stelligent/cfn_nag#per-resource-rule-suppression). All suppressed rules should have a valid justification. Add detailed information under `reason:` in the `Metadata` section of the template to avoid delays in the review process.
    
5. Run functional tests locally
    * **automated-security-helper *(ASH)* tests (this performs `cfn_nag` as well)**

    ```
    ## Executing ash tool

    $ git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

    # Set the repo path in your shell for easier access
    $ export PATH=$PATH:/tmp/ash

    $ ash --source-dir .
    $ cat aggregated_results.txt
    ```

    | **Note:** ASH tool is not part of the automated pipeline yet. If you are seeing this note, please include the output of the ASH tool file to your PR.|
    | --- |

    * **Run `taskcat` tests to deploy the templates**
        * Update the *.taskcat.yaml* in the root of the project. Refer to [taskcat documentation](https://aws-ia.github.io/taskcat/) for additional information. 
        * Update the default *.taskcat.yaml* file to closest to the below example:

    ```bash
    project:
    name: cfn-abi-aws-cloudtrail. # Change this to your project name
    owner: vinjak@amazon.com # Change to the owner
    package_lambda: true # Use this if you have lambda code in the repos
    shorten_stack_name: true # Recommended to use smaller stack names
    s3_regional_buckets: false # Not required if CopyZips are used. Refer to any ABI module for examples.
    regions:
    - us-east-1

    tests:
    enable-cloudtrail-org-level:
        regions:
        - us-east-1  # Control Tower Home region for Pilot
        template: templates/sra-cloudtrail-enable-in-org-ssm.yaml
        parameters:
        pSRASourceS3BucketName: $[taskcat_autobucket]
        pSRASourceS3BucketNamePrefix: $[taskcat_project_name]
        pSRAS3BucketRegion: us-east-1  # Bucket region. Keep it to us-east-1 as all the resources are deployed in the region.
        # ApiKey: $[taskcat_ssm_/path/to/ssm/parameter], update `taskcat_ssm_/path/to/ssm/parameter` as needed (^^).
    ```

    | (^^) **WARNING:** Do not include secrets like API Keys and Passwords in the parameters section of `.taskcat.yml` file. Refer to [PSUEDO_PARAMETERS](https://aws-ia.github.io/taskcat/docs/usage/PSUEDO_PARAMETERS/). Work with your AWS contact to securely make them available in the test environments.|
    | --- |

6. On successful completion of both static and functional tests in your local environment, publish the [Pull Request(PR)](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).

    ```
    git add <file-name>
    git commit -m <commit description>
    git push
    ```

7. Create a [Pull Request from your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
    
    **PS:** Wait until both internal and static tests complete, as shown below.

    ![Static Tests Success](/images/static_tests_complete.png)

    | **NOTE:** In case of test failure, choose *Details* to collect additional information|
    | --- |

8. Work with AWS PSA(*^*) to trigger functional tests. This can be done by adding `/do-e2e-tests` in the comments of the PR.
    ![Functional Tests](/images/functional-tests.png)

9. On successful completion of functional tests, the bot will add an approval. If the functional test fails, you will see an error, and you need to work with AWS PSA to get additional information on the failure.
|*E2E tests have completed successfully, however I am unable to provide an approval, as I opened this pr. You will need an additional human to review.*|
| --- |
11. A second approval needs to be given by an AWS personal. Once you have **2 approvals**, work with AWS PSA(*^*) to **Merge the pull request**.
    ![Change Approvals](/images/change-approval.png)

    | **NOTE:** Always [sync your fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork) to get the latest code and build your solution on top of it.|
    | --- |

(^) with write permissions to the repository

###### **Next:** Choose [Deployment Options](/deployment-options/index.html)