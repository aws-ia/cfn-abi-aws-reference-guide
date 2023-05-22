---
weight: 2
title: Overview
description: 
---


This ABI deploys <Partner project name> Integrations for AWS Organizations on the AWS Cloud. It’s for <persona-1> and <persona-2> that want to provide <partner-product-functionality> across multiple AWS accounts. If you are unfamiliar with AWS Built In, refer to the [AWS Built in](https://aws.amazon.com/builtin).

Deploying this ABI package does not guarantee an organization’s compliance with any laws, certifications, policies, or other regulations.


[Expand solution overview here]

### AWS Marketplace listing

[Partner-product-name-in-aws-marketplace](https://aws.amazon.com/marketplace/pp/prodview-<marketplace-id>)

**Next:** Choose [Terminologies](/terminologies/index.html) to get started.
=======
The AWS Built-in program is a differentiation program that validates Partner solutions which have automated their solution integrations with relevant AWS foundational services like identity, management, security and operations.  This program helps customers find and deploy a validated Partner solution that addresses specific customer use cases while providing deep visibility and control of AWS native service integration.

Utilizing AWS Built-In Partner software, customers can trust that the ISV product they are evaluating has been independently verified by AWS.

The program is focused across the four foundational service domains [Security, Identity, Management & Operations]. Partners who have existing IaC assets to deploy their solution and are part of the Security and CloudOps competency will be considered for a pilot to validate the value added by the ABI program. 

For example, when a customer subscribes to an ISV partner product, they need to follow a series of steps in order to transition from the subscription phase to a fully functional one. These steps include a combination of manual and IaC steps. Enabling services like [Amazon GuardDuty](https://aws.amazon.com/guardduty/), [AWS Security Hub](https://aws.amazon.com/security-hub/), [Amazon Inspector](https://aws.amazon.com/inspector/), and [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) before performing additional steps like adding AWS accounts, integrating with CloudTrail events and more on partner SaaS product.

With ABI packages, the partner leverages the AWS provided templates to enable AWS Services and add their additional logic on top of it. The customer can use these packages to reach full functionality in hours instead of days or weeks.

## Partner Workflow

AWS provides modules to enable AWS foundational services based on [AWS Security Reference Architecture (AWS SRA)](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html) guidelines. 

Partners can pick these modules and add additional logic to perform remaining steps like enabling partner integration in Security Hub or registering AWS account to partner product.

Once the solution is built, the partner can submit a Git Pull Request (PR) to the repository created for this project. 

All the PRs will go through a set of auto validations built-in to the pipelines. On successful completion of validation, the code is merged to the main branch of the repository, and published to other pre-defined targets.

![Partner Workflow](/images/partner_workflow.png)


## Customer workflow [Subjected to change]

![Customer Workflow](/images/customer_workflow.png)


### Terminologies

* **ABI :**   AWS Built In (ABI)  as explained above.
* **ABI Modules :** The GitHub repositories based of AWS SRA, which provide templates for enabling AWS foundational services like CloudTrail, GuardDuty, SecurityHub and more security services.
* **ABI Projects :** The GitHub repositories built by Partners in partnership with AWS. While building these projects, partners leverage ABI Modules provided to enable AWS services as needed before creating partner specific assets. The project contains 1\ IaC templates to automate enablement of both AWS and Partner services, 2\ Wrappers for most common formats like CfCT manifest, SC Baselines and more to allow customers to easily pick and choose from the services available. For Pilot, we will focus only on including CfCT manifest file in the package.
* **Project :** This is a GitHub repository for both ABI modules and ABI Projects
* **Project Owner :** The aliases of the 2‑5 Amazonians that will be granted administrative privileges to your AWS Builder Platform project.
* **Project Contributor :** Contributors are those that have been granted access to the project's code repository and can submit a Git Pull Request(PR). All non-AWS contributors will have read-only access to the repository. AWS contributors will have read/write access to the repository. 


### Architecture

![ABI Architecture](/images/abi-architecture.png)

When you submit a PR, there are set of automatic tests and manual validations that are performed. Following are the series of events that happen after PR.
1. **Static tests** are executed. The static tests include lint checkers, scan the templates and code provided against a set of pre- and custom-defined security rules to identify potential vulnerabilities. Tools used to run static tests are listed in [How to build an ABI project](docs/how-to-build-abi-project/index.html) section.
2. **Functional tests** on sucessful completion of static tests. You can comment `/do-e2e-tests` in the PR to kickoff the functional tests. The functional tests, deploys the tempaltes in the multi-account AWS environment associated with this repository. Tools used to run functional tests are listed in [How to build an ABI project](docs/how-to-build-abi-project/index.html) section.
3. **Bot Approval** is provided on successful completion of both static and functional tests. 
4. **Human Approval** by one of the AWS personal who have write permissions to the repository after sucessful PR review.
5. **Merge:** PR is merged to the main branch after clearing all 4 steps above.
6. **Publish:** the code is then automatically published to the targets.


#### Sample project layout

```
.
├── CODEOWNERS
├── CODE_OF_CONDUCT.md
├── LICENSE
├── NOTICE.txt
├── README.md
├── VERSION
├── docs
├── images
├── lambda_functions
│   └── source
│       └── enable_integrations
├── scripts
│   ├── cleanup_config.json
│   ├── cleanup_config.py
├── submodules  ## ABI Modules
│   └── cfn-abi-aws-securityhub
│       ├── README.md
│       ├── lambda_functions
│       ├── scripts
│       └── templates
└── templates  ## Partner build templates
    ├── abi-enable-partner1-securityhub-integration.yaml
    └── enable_integrations
        └── partner1-enable-integrations.yaml
```

#### How to get a GitHub repository

Work with with your AWS PSA contact to request for a repository. Once the project is approved, an ABI standard repository is created and invitation is shared with you. 

You need to Accept the invitation to get access to the repository.

#### How to build an ABI project 

[CLICK HERE](/how-to-build-abi-project/index.html) for steps. 

#### ABI deployment modes

* Launch the [CloudFormation Template in the Management Account](/launch-using-cloudformation/index.html).
* Launch using [Customizations for Control Tower (CfCT)](/launch-using-cfct/index.html).

## Things to know

* For Pilot, the existing modules are expected to operate only in AWS Control Tower environments. Hence, the modules provided as part of ABI should be deployed only in the ***Home Region of AWS Control Tower***.
* Follow the instructions in this [link](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacksets-orgs-enable-trusted-access.html) to enable trusted access for AWS CloudFormation StackSets with AWS Organizations via AWS CloudFormation StackSets console.
* Granting write permissions to GitHub repository is disabled by ABP when you add external contributors. This is required by AWS Security.
* For Pilot, the GitHub repositories remain private and GitHub IDs will be added manually.

## Cleanup Instructions

[CLICK HERE](/cleanup-instructions/index.html) for additional instructions. 


## Cost Considerations

[CLICK HERE](/cost-considerations/index.html) for steps. 

## FAQs

[CLICK HERE](/faqs/index.html) for additional information. 
