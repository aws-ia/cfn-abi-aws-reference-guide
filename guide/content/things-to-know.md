---
weight: 8
title: Things to know
description: Things you need to know about AWS Built-in
---

This section provides information on things that you need to know about AWS Built-in before you start building. Expect this section to get update constantly as we learn more about the requirements from our customers and partners.

* For the current release, the existing modules are expected to operate only in AWS Control Tower environments. Hence, the modules provided as part of ABI should be deployed only in the ***Home Region of AWS Control Tower***.
* Follow the instructions in this [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-enable-trusted-access.html) to enable trusted access for AWS CloudFormation StackSets with AWS Organizations via AWS CloudFormation StackSets console.
* Granting write permissions to GitHub repository is disabled by ABP when you add external contributors. This is required by AWS Security. Hence the external contributors will not be able to create branches or merge the code to the main branch. Work with your AWS PSA contact to get the code merged to the main branch.
* The GitHub repositories remain private until completion of the initial release.  Any GitHub IDs need to added manually to get access to the repository. Work with your AWS PSA contact to get access to the repository.


#### List of available ABI modules

|      AWS Service Name      |      Repository     |
| -------------------------- | ------------------- |
| AWS Security Hub           | [cfn-abi-aws-securityhub](https://github.com/aws-ia/cfn-abi-aws-securityhub) |
| AWS GuardDuty              | [cfn-abi-amazon-guardduty](https://github.com/aws-ia/cfn-abi-amazon-guardduty) |
| AWS Control Tower          | [cfn-abi-aws-cloudtrail](https://github.com/aws-ia/cfn-abi-aws-cloudtrail) |



**Next:** Choose [Common Patterns](/common-patterns/index.html).