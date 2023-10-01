---
weight: 4
title: Test Framework - Architecture
description: Architecture of the test framework
---

When you submit a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) (PR), a set of automatic tests and manual validations are performed. 

![ABI Architecture](/images/abi-architecture.png)

Below are the series of events that happen when you submit a PR:

1. **Internal tests** are executed. These tests are built and maintained by the Infrastructure and Automation team at AWS. These tests look for common security vulnerabilities and other common security issues.
2. **Static tests** are executed. The static tests include lint checkers, and scan templates/code provided against a set of pre- and custom defined security rules to identify potential vulnerabilities. Tools used are listed in the [How to build an ABI project](/how-to-build/index.html) section.
**PS:** Any errors on the Internal and Static tests will be reported as comments on the PR. You need to choose `Details` to view execution information. 
3. **Human verification** of the code by assigned AWS Partner Solutions Architects (PSA) team.
4. **Functional tests** on successful completion of static tests and manual review, AWS PSA(*^*) kickoff functional tests by commenting `/do-e2e-tests` in the PR. The functional tests, deploys the tempaltes in the multi-account AWS environment associated with this repository. Tools used are listed below.
5. **Bot Approval** will be provided on successful completion of both static and functional tests. 
6. **Human Approval**. AWS PSA(*^*) assgined to this project will review the test results of the functional tests and other security scanners and provide approval.
7. AWS PSA(*^*) will **Merge** the branch to the `main` branch once the above steps are cleared.
8. **Publish** the code is then automatically kicked off to the targets configured for each project.

*(^) with write permissions to the repository*

###### **Next:** Choose [Project Structure](/project-structure/index.html)
