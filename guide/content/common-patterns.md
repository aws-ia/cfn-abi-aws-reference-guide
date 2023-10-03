---
weight: 9
title: Common patterns
description: This document provides common patterns that can be used to build an ABI project.
---

This section calls out some of the common patterns (including technical code samples) that are used in multiple partner solutions. This will be updated as we learn more about the requirements from our customers and partners.

### CloudTrail ABI Module - Common Patterns

In this section, we will look at some of the common usage patterns that can be used to build the ABI projects. This is not a replacement for the [ABI CloudTrail Module documentation](https://github.com/aws-ia/cfn-abi-aws-cloudtrail#readme) available with the module. This is just a quick reference to help you get started with the ABI CloudTrail Module.

The CloudTrail ABI module, allows you to create an Organization CloudTrail within the Organization Management Account that is encrypted with a Customer Managed KMS Key managed in the **Audit Account** and logs delivered to the **Log Archive Account**. An Organization CloudTrail logs all events for all AWS accounts in the AWS Organization.

When you create an organization trail, a trail with the name that you give it will be created in every AWS account that belongs to your organization. Users with CloudTrail permissions in member accounts will be able to see this trail when they log into the AWS CloudTrail console from their AWS accounts, or when they run AWS CLI commands such as describe-trail.

The solution default configuration deploys an Organization CloudTrail enabling **data events ONLY** to avoid duplicating the existing AWS Control Tower CloudTrail, which has the management events enabled.

You can optionally enable **management events ONLY** for the Organization CloudTrail by setting the `pEnableDataEventsOnly` parameter to `False`. See below for common patterns.

##### Pattern 1: Enable Organization CloudTrail with management events only

The following template snippet is the minimum parameter required to enable Organization CloudTrail with management events only. You may leave the remaining parameters to *default* values.

```yaml
  rCloudTrailManagementEventsOnly:
    Type: 'AWS::CloudFormation::Stack'
    Properties:
      TemplateURL: !Sub >-
        https://${pSRASourceS3BucketName}.s3.${pSRAS3BucketRegion}.${AWS::URLSuffix}/${pSRAStagingS3KeyPrefix}/submodules/cfn-abi-aws-cloudtrail/templates/sra-cloudtrail-enable-in-org-ssm.yaml
      Parameters:
        pEnableDataEventsOnly: 'false'
        pSRASourceS3BucketName: !Ref pSRASourceS3BucketName
        pSRAS3BucketRegion: !Ref pSRAS3BucketRegion
        pSRAStagingS3KeyPrefix: !Ref pSRAStagingS3KeyPrefix
```

##### Pattern 2: Enable Organization CloudTrail with data events only

The following template snippet is the minimum parameter required to enable Organization CloudTrail with data events only. You may leave the remaining parameters to *default* values.

```yaml
  rCloudTrailDataEventsOnly:
    Type: 'AWS::CloudFormation::Stack'
    Properties:
      TemplateURL: !Sub >-
        https://${pSRASourceS3BucketName}.s3.${pSRAS3BucketRegion}.${AWS::URLSuffix}/${pSRAStagingS3KeyPrefix}/submodules/cfn-abi-aws-cloudtrail/templates/sra-cloudtrail-enable-in-org-ssm.yaml
      Parameters:
        pEnableDataEventsOnly: 'true'
        pSRASourceS3BucketName: !Ref pSRASourceS3BucketName
        pSRAS3BucketRegion: !Ref pSRAS3BucketRegion
        pSRAStagingS3KeyPrefix: !Ref pSRAStagingS3KeyPrefix

```

##### Scenario 1 : For partner integrations that leverage ABI CloudTrail module

We recommend providing an option in your main template to enable the CloudTrail module. Keep this option **disabled by default**. Considering the cost associated with CloudTrail when a second trail is created unintentionally, we recommend having this option disabled by default and let customers choose to enable this option.

This allows the customers who do not have the CloudTrail trails enabled, to enable it as part of the deployment of your solution.

The following template snippet provides a sample of achieving it.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: CloudTrail Module Properties
        Parameters:
          - pEnableCloudTrail
          - pEnableS3DataEvents

    ParameterLabels:
      pEnableCloudTrail:
        default: Enable CloudTrail Organization Trail?
      pEnableS3DataEvents:
        default: Enable CloudTrail S3 Data Events for all buckets or management accounts?

Parameters:
  pEnableCloudTrail:
    AllowedValues: ['true', 'false']
    Default: 'false'
    Description: Enable CloudTrail
    Type: String
  pEnableS3DataEvents:
    AllowedValues: ['true', 'false']
    Default: 'false'
    Description: Enable CloudTrail S3 Data Events for all buckets
    Type: String

Conditions:
  cEnableCloudTrail: !Equals [!Ref pEnableCloudTrail, 'true']


Resources:
  rCloudTrailEnableInOrg:
    Type: 'AWS::CloudFormation::Stack'
    Condition: cEnableCloudTrail
    DeletionPolicy: Delete
    UpdateReplacePolicy: Delete
    Properties:
      TemplateURL: !Sub https://${pSRASourceS3BucketName}.s3.${pSRAS3BucketRegion}.${AWS::URLSuffix}/${pSRAStagingS3KeyPrefix}/submodules/cfn-abi-aws-cloudtrail/templates/sra-cloudtrail-enable-in-org-ssm.yaml
      Parameters:
        pSRASourceS3BucketName: aws-abi
        pSRAStagingS3KeyPrefix: cfn-abi-aws-cloudtrail
        pEnableS3DataEvents: !Ref pEnableS3DataEvents
      Tags:
        - Key: sra-solution
          Value: !Ref pSRAStagingS3KeyPrefix
```

### GuardDuty ABI Module - Common Patterns

In this section, we will look at some of the common usage patterns that can be used to build the ABI projects. This is not a replacement for the [ABI GuardDuty Module documentation](https://github.com/aws-ia/cfn-abi-amazon-guardduty#readme) available with the module. This is just a quick reference to help you get started with the ABI GuardDuty Module.

The sample code provided in the GuardDuty module accomplishes the following:

   * Enables GuardDuty for all AWS accounts that are current members of the target organization in AWS Organizations

   * Turns on the Auto-Enable feature in GuardDuty, which automatically enables GuardDuty for any accounts that are added to the target organization in the future

   * Allows you to select the Regions where you want to enable GuardDuty

   * Uses the organization’s Audit account as the GuardDuty delegated administrator

   * Creates an Amazon Simple Storage Service (Amazon S3) bucket in the logging account and configures GuardDuty to publish the aggregated findings from all accounts in this bucket

   * Assigns a life-cycle policy that transitions findings from the S3 bucket to Amazon S3 Glacier Flexible Retrieval storage after 365 days, by default

   * Enables GuardDuty S3 protection and EKS protection, by default

**NOTE-1**: If the solution is deployed outside `us-east-1` region, there are few additional steps required. Please refer to the [Installation workflow documentation](https://github.com/aws-ia/cfn-abi-amazon-guardduty#installation-workflow) from the ABI GuardDuty Module for more details.

**NOTE-2**: There is a known issue with the GuardDuty module, when `pAutoEnableMalwareProtection` is set to `true`. Please leave this option to `false` until the issue is resolved. We will update this document once the issue is resolved.

#### For partner integrations that leverage ABI GuardDuty module

The following template snippet is the minimum parameter required to enable GuardDuty. You may leave the remaining parameters to *default* values, unless your product needs additional options supported by the ABI module. Please refer to the Descriptions of each parameter in the template for additional details.

We recommend providing an option in your main template to enable the GuardDuty module. Keep this option **disabled by default**. If the customer already has GuardDuty enabled in their environments, trying to enable GuardDuty again will lead to stack failures. 

This allows the customers who do not have the GuardDuty trails enabled at organization level, to enable it as part of the deployment of your solution.

The following template snippet provides a sample of achieving it.

```yaml
Metadata:
  AWS::CloudFormation::Interface:
    ParameterGroups:
      - Label:
          default: GuardDuty Module Properties
        Parameters:
          - pEnableGuardDuty
          - pAutoEnableS3Logs
          - pAutoEnableK8sLogs
          - pAutoEnableMalwareProtection
    ParameterLabels:
      pEnableGuardDuty:
        default: Enable GuarDuty at Organization level
      pAutoEnableS3Logs:
        default: Auto Enable S3 Logs
      pAutoEnableK8sLogs:
        default: Auto Enable kubernetes Logs
      pAutoEnableMalwareProtection:
        default: Auto Enable malware protection

Parameters:
  pEnableGuardDuty:
    AllowedValues: ['true', 'false']
    Default: 'false'
    Description: Enable GuardDuty at Organization level
    Type: String
  pAutoEnableS3Logs:
    AllowedValues:
      - 'true'
      - 'false'
    Default: 'true'
    Description: Auto enable S3 logs
    Type: String
  pAutoEnableK8sLogs:
    AllowedValues:
      - 'true'
      - 'false'
    Default: 'false'
    Description: Auto Enable kubernetes Logs
    Type: String
  pAutoEnableMalwareProtection:
    AllowedValues:
      - 'true'
      - 'false'
    Default: 'false'
    Description: Auto Enable malware protection
    Type: String

Conditions:
  cEnableGuardDuty: !Equals [!Ref pEnableGuardDuty, 'true']

Resources:
  rGuardDutyEnableInOrg:
    Type: 'AWS::CloudFormation::Stack'
    Condition: cEnableGuardDuty
    DeletionPolicy: Delete
    UpdateReplacePolicy: Delete
    Properties:
      TemplateURL: !Sub https://${pSRASourceS3BucketName}.s3.${pSRAS3BucketRegion}.${AWS::URLSuffix}/${pSRAStagingS3KeyPrefix}/submodules/cfn-abi-amazon-guardduty/templates/sra-guardduty-enable-in-org-ssm.yaml
      Parameters:
        pAutoEnableS3Logs: !Ref pAutoEnableS3Logs
        pAutoEnableK8sLogs: !Ref pAutoEnableK8sLogs
        pAutoEnableMalwareProtection: !Ref pAutoEnableMalwareProtection
        pSRASolutionName: !Ref pSRASolutionName
        pSraTestingFlag: !Ref pSraTestingFlag
        pSRAS3BucketRegion: !Ref pSRAS3BucketRegion
```

**Next:** Choose [FAQs](/faqs/index.html).