---
weight: 8
title: Deployment Steps
description: Step-by-step instructions for deploying the <project-name>.
---

## Launch the CloudFormation template in the management account


1. Download the Cloudformation template from the following location: https://<abi-template-location>
2. Launch CloudFormation template in your AWS Control Tower home region.
    * Stack name: `template-<partner-name>-enable-integrations`
    * List parameters with [default values and update below example as needed]
        * **EnableIntegrationsStackName**: `template-<partner-name>-enable-integrations`
        * **EnableIntegrationsStackRegion**: `us-east-1`
        * **EnableIntegrationsStackSetAdminRoleName**: `AWSCloudFormationStackSetAdministrationRole`
        * **EnableIntegrationsStackSetExecutionRoleName**: `AWSCloudFormationStackSetExecutionRole`
        * **EnableIntegrationsStackSetExecutionRoleArn**: `arn:aws:iam::<account-id>:role/AWSCloudFormationStackSetExecutionRole`

3. Select both the **Capabilities** and choose **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND    

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.


## Launch using Customizations for Control Tower

[Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/) (CfCT) combines AWS Control Tower and other AWS services to help you set up an AWS environment. You can deploy the templates provided with the ABI solution using CfCT.

The templates provided as part of the ABI solution are deployable using Customizations for Control Tower. Please check below for additional details.

#### Pre-requisites

1. The CfCT solution, do not have ability to launch resources on the Management account. Hence, you need to create the role with required permissions in the Management account.

#### How it works

To deploy the sample partner integration page using CfCT solution, add the following blurb to the `manifest.yaml` file from your CfCT solution and then update the account and organizational unit (OU) names as needed.

```
resources:
  - name: sra-enable-partner1-solution
    resource_file: https://aws-abi-pilot.s3.us-east-1.amazonaws.com/cfn-abi-aws-reference-guide/templates/abi-enable-partner1-securityhub-integration.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: pProductArn
        parameter_value: arn:aws:securityhub:us-east-1::product/cloud-custodian/cloud-custodian
      - parameter_key: pSRASourceS3BucketName
        parameter_value: aws-abi-pilot
      - parameter_key: pSRAStagingS3KeyPrefix
        parameter_value: cfn-abi-aws-reference-guide
    deployment_targets:
      accounts:
        - [[MANAGEMENT-AWS-ACCOUNT-ID]]
```
## Partner specific steps [UPDATE AS NEEDED]
After the stack deployment is complete, verfiy following resources [....]:

  - <resource-1>
  - <resource-2>

Open <partner-console> and navigate to <section> and perform following steps:
   1. <step-1>
   2. <step-2>


**Next:** Go to [Postdeployment steps](/post-deployment-steps/index.html) to verify the deployment.