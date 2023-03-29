## How to build an ABI project 

1. Once you have access to the reposity, clone it to your local environment

    ```
    git clone https://github.com/aws-ia/<your-repo-name>.git
    ```

2. Create branch `devel` to start developing your project.
    ```
    cd <your-repo-name>
    ```
    ```
    git checkout -b devel
    git branch
    ```
3. Add the required ABI Modules as submodules to your repository (example below to add securityhub repo). 
    ```
    mkdir submodules
    cd submodules
    git submodule add https://github.com/aws-ia/cfn-abi-aws-securityhub.git
    ```
    List of all available ABI Modules are [Available here](https://link-to-be-added).
4. Build and update the code as per your project needs. Following directort hierarchy as shown below:

    ```
        .
    ├── docs # Directory to include additional documentation
    ├── images # Directory to include images used in the documentation
    ├── lambda_functions # Directory for storing lambda code
    │   ├── packages
    │   └── source
    ├── scripts
    ├── submodules # Directory for ABI modules
    │   └── cfn-abi-aws-securityhub
    │       ├── images
    │       ├── lambda_functions
    │       │   └── source
    │       ├── scripts
    │       └── templates
    │           ├── functions
    │           ├── scripts
    │           ├── sra-securityhub-org
    │           └── sra-sh-prerequisites
    └── templates # Directory for storing IaC templates
        ├── functions
        │   └── source
        └── scripts
    ```
5. Run static tests locally.

    Execute following tests locally  in your environment, the same set of tests are executed as part of the pipeline validations done with these tests:

    * **cfn-lint tests:**

        ```
        pip3 install cfn-lint
        ```

    * **taskcat lint:**

        ```
        pip3 install taskcat
        ```

    * **cfn-nag tests and add exceptions if needed**

        https://github.com/stelligent/cfn_nag

6. Run functional tests locally
    * **automated-security-helper *(ASH)* tests (this performs `cfn_nag` as well)**

        ```
        ## Executing ash tool

        $ git clone https://github.com/aws-samples/automated-security-helper.git /tmp/ash

        # Set the repo path in your shell for easier access
        $ export PATH=$PATH:/tmp/ash

        $ ash --source-dir .
        $ cat aggregated_results.txt
        ```
    * **Run `taskcat` tests to deploy the templates**
        * Update the .taskcat.yaml in the root of the project. Additional information [available here](https://aws-ia.github.io/taskcat/)
        * Update the default .taskcat.yaml file to closest to below example:

        ```
        project:
        name: cfn-abi-aws-cloudtrail. # Change this to your project name
        owner: vinjak@amazon.com # Change to the owner
        package_lambda: true # Use this if you have lambda code in the repos
        shorten_stack_name: true # Recommended to use smaller stack names
        s3_regional_buckets: false # Not required if CopyZips are used. Refer to any ABI module for examples.
        regions:
        - us-west-2

        tests:
        enable-cloudtrail-org-level:
            regions:
            - us-west-2  # Control Tower Home region for Pilot
            parameters:
            pSRASourceS3BucketName: $[taskcat_autobucket]
            pSRASourceS3BucketNamePrefix: $[taskcat_project_name]
            pSRAS3BucketRegion: us-east-1  # Bucket region. Keep it to us-east-1 as all the resources are deployed in the region.
            template: templates/sra-cloudtrail-enable-in-org-ssm.yaml
        ```

7. On successful completion of both static and functional tests in your local environment, publish the PR.

    ```
    git add <file-name>
    git commit -m <commit description>
    git push
    ```

8. Create a Pull Request in the GitHub repository

    ![Create Pull Request](/images/create_pull_request.png)
    
    **PS: ** Wait until the static tests are complete as shown below.

    ![Static Tests Success](/images/static_tests_complete.png)

9. Trigger functional tests by adding `/do-e2e-tests` in the comments.
    ![Functional Tests](/images/functional-tests.png)

10. On successful completion of functional tests, bot will add an approval.

11. A second approval need to be given by an AWS personal. Once you have **2 approvals**, you can **Merge pull request**.
    ![Change Approvals](/images/change-approval.png)

    **NOTE:** Delete the branch once merge as a good practice. A new branch can be made off of the most recent commit on the master branch.
    ![](/images/Merge-PR-Delete-Branch.png)
