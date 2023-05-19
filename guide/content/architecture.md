---
weight: 5
title: Architecture
description: Solution architecture.
---

Deploying this ABI package with default parameters builds the following architecture.

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

**Next:** Choose [Deployment Options](/deployment-options/index.html) to get started.