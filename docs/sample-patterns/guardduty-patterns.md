### CloudTrail ABI Module - Common Patterns

In this section, we will look at some of the common usage patterns that can be used to build the ABI projects. This is not a replacement to the [ABI GuardDuty Module documentation](https://github.com/aws-ia/cfn-abi-amazon-guardduty#readme) available with the module. This is just a quick reference to help you get started with the ABI GuardDuty Module.

The sample code provided in the GuardDuty module accomplishes the following:

   * Enables GuardDuty for all AWS accounts that are current members of the target organization in AWS Organizations

   * Turns on the Auto-Enable feature in GuardDuty, which automatically enables GuardDuty for any accounts that are added to the target organization in the future

   * Allows you select the Regions where you want to enable GuardDuty

   * Uses the organization’s Audit account as the GuardDuty delegated administrator

   * Creates an Amazon Simple Storage Service (Amazon S3) bucket in the logging account and configures GuardDuty to publish the aggregated findings from all accounts in this bucket

   * Assigns a life-cycle policy that transitions findings from the S3 bucket to Amazon S3 Glacier Flexible Retrieval storage after 365 days, by default

   * Enables GuardDuty S3 protection and EKS protection, by default

**NOTE-1**: If the solution is deployed outside `us-east-1` region, there are few additional steps required. Please refer to the [Installation workflow documentation](https://github.com/aws-ia/cfn-abi-amazon-guardduty#installation-workflow) from the ABI GuardDuty Module for more details.

**NOTE-2**: There is a known issue with the GuardDuty module, when `pAutoEnableMalwareProtection` is set to `true`. Please leave this option to `false` until the issue is fixed. We will update this document once the issue is fixed.

#### For partner integrations that leverage ABI GuardDuty module

Following template snippet is the mimimum parameter required to enable Guardduty. You may leave the remaining parameters to *default* values unless your product needs additional options supported by the ABI module. Please refer to the Descriptions of each parameter in the template for additional details.

We recommend to provide an option in your main template to enable the GuardDuty module. Keep this option **disabled by default**. If the customer already have GuardDuty enabled in their environments, trying to enable guardduty again will lead to the stack failures. 

This allows the customers who do not have the GuardDuty trails enabled at organization level, to enable it as part of the deployment of your solution.

Following template snippet provides a sample of achieving it.

```
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