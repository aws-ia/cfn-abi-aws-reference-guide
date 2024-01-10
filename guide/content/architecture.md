---
weight: 5
title: Architecture
description: Solution architecture.
---

Deploying this ABI with default parameters builds the following architecture.

![Architecture diagram](/images/architecture.png)

As shown in the diagram, the Quick Start sets up the following:

* In all current and AWS accounts in your AWS organization:
    * <Amazon CloudWatch Events rules> to <detect changes in AWS Config configuration items (CIs)> and <trigger AWS Lambda functions>.
    * <Service> to perform <Action-1> and <Action-2>.

* In the management account:
    * <Service> to perform <Action-1> and <Action-2>.

* In the log archive account:
    * <Service> to perform <Action-1> and <Action-2>.

* In the security tooling account:
    * <Service> to perform <Action-1> and <Action-2>.

## Architecture overview

The <project-name> integration establishes a connection between <product-name> and your AWS environment. <product-name> uses IAM roles and policies to access and collect security-related data from your AWS accounts.

The deployment of the <project-name> is automated using AWS CloudFormation. CloudFormation templates are used to provision the required resources, including IAM roles, S3 buckets,[....], and [....].

<product-name> collects [....] from various AWS services, such as <service-1>, <service-2>, and <service-3>. These events are processed and analyzed by <product-name>’s to provide additional capabilities like [....].

Based on the information collected, <product-name> provides [....] to improve [....] of your AWS environment. These findings help you perform [....].

**Next:** See [Deployment options](/deployment-options/index.html) to get started.