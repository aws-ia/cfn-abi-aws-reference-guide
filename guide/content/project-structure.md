---
weight: 5
title: ABI Project Structure
description: Repository hirearchy
---

When a project proposal is approved AWS Built-in team will create following resources before you get started with the project. 

1. GitHub repository
2. Permissions to the repository for nominated contributors.
2. A Test environment with 3 AWS accounts dedicated for this project.

If you are an AWS Partner, you need to work with an AWS PSA assgined for this project for any questions or issues.

**PS:** Only AWS PSAs will have access to the test environment and the accounts. 

The internal and static test failures are reported in the GitHub console and contributors can review the logs from there. However, for functional tests, only the test status is reported. If you need to review the logs for troubleshooting purposes, you need to work with the AWS PSA assigned for this project.

When a project repository is created, it will be bootstrapped with the following files and folders: 

```bash
.
├── CODEOWNERS
├── CODE_OF_CONDUCT.md
├── LICENSE
├── NOTICE.txt
├── VERSION
├── .taskcat.yml ## FILE TO DEFINE TEST CASES. USED BY THE TEST FRAMEWORK
├── lambda_functions 
│   └── source ## FOLDER TO STORE LAMBDA FUNCTIONS
│   │   └── enable_integrations
│   │     ├── my_custom_function.py
│   │     └── requirements.txt ## FILE TO DEFINE DEPENDENCIES. USED DURING CREATION OF LAMBDA PACKAGE
│   └── packages ## THIS FOLDER AND CONTENT IS CREATED BY BUILD PROCESS. DO NOT CREATE.
│       └── enable_integrations
│         └── lambda.zip
├── scripts ## CLEANUP UTILITIES, USED BY THE TEST FRAMEWORK
│   ├── cleanup_config.json
│   ├── cleanup_config.py
├── submodules
│   └── aws-security-reference-architecture-examples
│       ├── AWS-SRA-KEY-INFO.md
│       ├── CHANGELOG.md
│       ├── LICENSE
│       ├── README.md
│       ├── aws_sra_examples
│       │   ├── docs
│       │   ├── easy_setup
│       │   ├── modules
│       │   │   ├── cloudtrail-org-module
│       │   │   ├── guardduty-org-module
│       │   │   └── securityhub-org-module
│       │   ├── quick_setup
│       │   ├── solutions
│       │   └── utils
│       └── pyproject.toml
└── templates  ## FOLDER TO STORE INFRASTRUCTURE AS CODE TEMPLATES
    ├── abi-enable-partner1-securityhub-integration.yaml
    └── enable_integrations
        └── partner1-enable-integrations.yaml
```


###### **Next:** Choose [How to build an ABI Project](/how-to-build/index.html)