---
weight: 2
title: AWS Built-in Overview
description: 
---

[AWS Built-in](https://aws.amazon.com/partners/built-in-partner-solutions/)(ABI) is a validated program awarded to ISV Partners to help customers deploy 3rd party software integrated with AWS Native Services. Target customers prefer to buy a turnkey solution versus installing, securing, and configuring AWS Native Services themselves in order to realize the full benefits of 3rd party software. Partner owned Built-in offerings provide deployment packages where partner solutions are integrated with AWS services via IaC, which reduces the time customers spend from weeks to minutes and helps increase customer efficiency by optimizing the time to deploy new initiatives.

AWS built-in partner solutions install, configure, and integrate with key foundational AWS services using a well-architected Modular Code Repository (MCR) in an automated deployment package validated by AWS experts, increasing time to value. This automated integration is independently verified by AWS and saves hours, days, or even weeks of vendor integration testing.

By streamlining the integration process, we empower customers to fully harness the benefits of foundational AWS native services while taking advantage of the rich functionality and capabilities of third-party solutions. Our objective is to facilitate a unified and cohesive experience for customers, eliminating the complexities associated with combining different software and data sources.

For example, when a customer subscribes to an ISV partner product, they must follow a series of steps in order to transition from the subscription phase to a fully functional phase. These steps include a combination of manual and IaC steps. Enabling services like [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS Security Hub](https://aws.amazon.com/security-hub/), [Amazon Inspector](https://aws.amazon.com/inspector/), and [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) before performing additional steps like adding AWS accounts, integrating with CloudTrail events and more on partner SaaS product.

### Terminologies

* **ABI :** AWS Built-in (ABI) as explained above.
* **ABI Modules :** The GitHub repositories based of [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html) (AWS SRA), which provide templates for enabling AWS foundational services like CloudTrail, GuardDuty, and SecurityHub.
* **ABI Project :** The GitHub repositories built by Partners in partnership with AWS. While building these projects, partners leverage ABI Modules provided to enable AWS services as needed before creating partner specific assets. The project contains:
    1. IaC templates to automate enablement of both AWS and Partner services, 
    2. Wrappers for most common formats like CfCT manifest, 
    3. AWS Service Catalog baselines to allow customers to easily pick and choose from the services available. 
For Pilot, we will focus only on including CfCT manifest file in the package.
* **Project Owner :** are users who can add contributors, change/approve permissions, and more.
* **Project Contributor :** Contributors are those that have been granted access to the project's code repository.
* **Repository permissions :** GitHub permissions assigned to repo contributors. There are **READ** and **WRITE** permissions. 
* Contributors with **READ** permissions need to fork the project, work on their fork and submit a PR. They will not be able to create a branch on the main repo, or run functional tests, or merge PRs.
* Contributors with **WRITE** permissions can read and make changes to the project. They can create branches in the main repo, run functional tests, and merge PRs.
* An external (non-Amazon) contributor will only have **READ** permissions.

###### **Next:** Choose [Workflows](/workflows/index.html)