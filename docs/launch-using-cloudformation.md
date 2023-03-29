## Launch ABI using CloudFormation Templates

Launch the cloudformation template provided as part <project-root>/templates/ in the Management Account of the organization.


1. Download the cloudformation template from source: https://aws-abi-pilot.s3.us-east-1.amazonaws.com/cfn-abi-aws-reference-guide/templates/abi-enable-partner1-securityhub-integration.yaml
2. Launch CloudFormation template in your AWS Control Tower home region.
    * Stack name: `launch-abi-sample-partner-integration`
    * ARN of partner integration to turn on in AWS Security Hub: `arn:aws:securityhub:$[taskcat_current_region]::product/cloud-custodian/cloud-custodian`
    * Leave the remaining values default.
3. Choose both the **Capabilities** and select **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND    

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.