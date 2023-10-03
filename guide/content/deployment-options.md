---
weight: 7
title: Deployment Options
description: AWS Biult-in Deployment Options
---

We learned from our customers operating in multi-account environments that they often have a customized deployment methods to manage their Infrastructure as Code (IaC) templates. They want to apply the same methodologies for entire infrastructure including  AWS services, on-permises, or Partner products. 

As part of AWS Built-in, we build the least possible denominator that can be used with multiple deployment options. Following are a few commonly used deployment options, we support in the current release:

1. Launch using CloudFormation Template in the Management Account.
2. Launch using Customizations for Control Tower (CfCT).

While we try to provide as many options as possible, we understand that we may not be able to cover all the deployment options. We are working on adding more deployment options based on the feedback. If you have a specific deployment option that you would like to see, please reach out to your AWS contact or open an issue in this GitHub repository.


## Launch ABI using CloudFormation Templates

Launch the CloudFormation template provided as part <project-root>/templates/ in the Management Account of the organization.

1. Login to your Management Account to deploy this ABI package.
2. Choose [Launch Stack](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/new?stackName=launch-abi-sample-partner-integration&templateURL=https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-aws-reference-guide/templates/abi-enable-partner1-securityhub-integration.yaml) and change the AWS Region to your AWS Control Tower home region.
3. Choose **Next**.
4. Type value to **ARN of partner integration to turn on in AWS Security Hub:** `arn:aws:securityhub:$[taskcat_current_region]::product/cloud-custodian/cloud-custodian` and leave the remaining values default.
5. Choose both the **Capabilities** and select **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND    

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.

## Launch ABI using Customizations for Control Tower (CfCT)

[Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/) combines AWS Control Tower and other highly-available, trusted AWS services to help customers more quickly set up a secure, multi-account AWS environment using AWS best practices. You can easily add customizations to your AWS Control Tower landing zone using an AWS CloudFormation template and service control policies (SCPs). You can deploy the custom template and policies to individual accounts and organizational units (OUs) within your organization. It also integrates with AWS Control Tower lifecycle events to ensure that resource deployments stay in sync with your landing zone. For example, when a new account is created using the AWS Control Tower account factory, Customizations for AWS Control Tower ensures that all resources attached to the account's OUs will be automatically deployed.

The templates provided as part of the ABI packages are deployable using Customizations for Control Tower. Please check below for additional details.

##### Pre-requisites

1. The CfCT solution, do not have ability to launch resources on the Management account. Hence, you need to create the role with required permissions in the Management account.

##### How it works

To deploy this sample partner integration page using CfCT solution, add the following blurb to the `manifest.yaml` file from your CfCT solution and update the account/ou names as needed.

```yaml
resources:
  - name: sra-enable-partner1-solution
    resource_file: https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-aws-reference-guide/templates/abi-enable-partner1-securityhub-integration.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: pProductArn
        parameter_value: arn:aws:securityhub:us-east-1::product/cloud-custodian/cloud-custodian
      - parameter_key: pSRASourceS3BucketName
        parameter_value: aws-abi
      - parameter_key: pSRAStagingS3KeyPrefix
        parameter_value: cfn-abi-aws-reference-guide
    deployment_targets:
      accounts:
        - [[MANAGEMENT-AWS-ACCOUNT-ID]]
```

**Next:** Choose [Things to know](/things-to-know/index.html).