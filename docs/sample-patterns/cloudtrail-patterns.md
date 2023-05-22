### CloudTrail ABI Module - Common Patterns

In this section, we will look at some of the common usage patterns that can be used to build the ABI projects. This is not a replacement to the [ABI CloudTrail Module documentation](https://github.com/aws-ia/cfn-abi-aws-cloudtrail#readme) available with the module. This is just a quick reference to help you get started with the ABI CloudTrail Module.

The CloudTrail ABI module, allows you to create an Organization CloudTrail within the Organization Management Account that is encrypted with a Customer Managed KMS Key managed in the **Audit Account** and logs delivered to the **Log Archive Account**. An Organization CloudTrail logs all events for all AWS accounts in the AWS Organization.

When you create an organization trail, a trail with the name that you give it will be created in every AWS account that belongs to your organization. Users with CloudTrail permissions in member accounts will be able to see this trail when they log into the AWS CloudTrail console from their AWS accounts, or when they run AWS CLI commands such as describe-trail.

The solution default configuration deploys an Organization CloudTrail enabling **data events ONLY** to avoid duplicating the existing AWS Control Tower CloudTrail, which has the management events enabled.

You can optionally enable **management events ONLY** for the Organization CloudTrail by setting the `pEnableDataEventsOnly` parameter to `False`. See below for common patterns.

#### Pattern 1: Enable Organization CloudTrail with management events only

Following template snippet is the minimum parameter required to enable Organization CloudTrail with management events only. You may leave the remaining parameters to *default* values.

```
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

#### Pattern 2: Enable Organization CloudTrail with data events only

Following template snippet is the minimum parameter required to enable Organization CloudTrail with data events only. You may leave the remaining parameters to *default* values.

```
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

#### Scenario 1 : For partner integrations that leverage ABI CloudTrail module

We recommend to provide an option in your main template to enable the CloudTrail module. Keep this option **disabled by default**. Considering the cost associated with CloudTrail when second trail is created unintentionally, we recommend to have this option disabled by default and let customers choose to enable this option.

This allows the customers who do not have the CloudTrail trails enabled, to enable it as part of the deployment of your solution.

Following template snippet provides a sample of achieving it.

```
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
        pSRASourceS3BucketName: aws-abi-pilot
        pSRAStagingS3KeyPrefix: cfn-abi-aws-cloudtrail
        pEnableS3DataEvents: !Ref pEnableS3DataEvents
      Tags:
        - Key: sra-solution
          Value: !Ref pSRAStagingS3KeyPrefix
```