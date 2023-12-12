---
weight: 8
title: Things to know
description: Things you need to know about AWS Built-in
---

This section provides information on things that you need to know about AWS Built-in before you start building. Expect this section to get updated constantly as we learn more about the requirements from our customers and partners.

The following steps are applicable for both partners and customers. Partners who are building the solution should follow guidelines when deploying an ABI package in any AWS environment. In addition, include these in the repository documentation.

* For the current release, the existing modules are expected to operate only in AWS Control Tower environments. Hence, the modules provided as part of ABI should be deployed only in the ***Management Account*** within the ***Home Region of AWS Control Tower***.
* Follow the instructions in this [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-enable-trusted-access.html) to enable trusted access for AWS CloudFormation StackSets with AWS Organizations via AWS CloudFormation StackSets console.

The guidelines below don't apply to customers; they only apply to the partners who are building the solution.

* Granting write permissions to GitHub repository is disabled by ABP when you add external contributors. This is required by AWS Security. Hence, the external contributors will not be able to create branches or merge the code to the main branch. Work with your AWS PSA contact to get the code merged to the main branch.
* The GitHub repositories remain private until completion of the initial release.  Any GitHub IDs need to added manually to get access to the repository. Work with your AWS PSA contact to get access to the repository.


#### List of available ABI / SRA modules

|      AWS Service Name      |      Repository     |
| -------------------------- | ------------------- |
| SRA Modules (MOD_ROOT)           | [aws-security-reference-architecture-examples/aws-sra-examples/modules](https://github.com/aws-samples/aws-security-reference-architecture-examples/tree/main/aws_sra_examples/modules) |
| AWS Security Hub           | [${MOD_ROOT}/securityhub-org-module](https://github.com/aws-samples/aws-security-reference-architecture-examples/tree/main/aws_sra_examples/modules/securityhub-org-module/templates) |
| AWS GuardDuty              | [${MOD_ROOT}/guardduty-org-module](https://github.com/aws-samples/aws-security-reference-architecture-examples/tree/main/aws_sra_examples/modules/guardduty-org-module/templates) |
| AWS Control Tower          | [${MOD_ROOT}/cloudtrail-org-module](https://github.com/aws-samples/aws-security-reference-architecture-examples/tree/main/aws_sra_examples/modules/cloudtrail-org-module/templates) |


**Next:** Choose [Common Patterns](/common-patterns/index.html).