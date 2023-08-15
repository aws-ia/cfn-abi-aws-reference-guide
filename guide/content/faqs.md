---
weight: 100
title: FAQs
description: Frequently asked questions
---

## Can I contribute to this repository? 

Yes, this shared under Apache License, version 2.0 (the "License"). Please submit a GitHub issue if you see an issues or improvements. If you like to build and contribute a fix or enhancement, please submit a GitHub pull request with your changes.

All pull requests will go through auto validations and human reviews before it is merged.

## How to add internal AWS contributors? 

Access to the repositories are controlled from the builder platform interface. Refer to [ABP usage guide](https://yet-to-be-built) for steps.

## How to add contributors from partner side?

Use the same mechanism mentioned above to manage access to the repository. If you are a partner trying to access these repos, reach out your assigned AWS PSA.

## How do I add secrets to the parameters in the taskcat file?

Our preferred way is to pass the parameter as SSM_Parameter value and pass it as [$[taskcat_ssm_/path/to/ssm/parameter]](https://aws-ia.github.io/taskcat/docs/usage/PSUEDO_PARAMETERS/) as a value. While testing locally, make sure to [create the parameter](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html) in your account/region that you are testing. When you check-in the code, reach out to your AWS contact to facilate this setup in your test environment. 

## Why is my ASH tool failing?

A: Please make sure you have docker running in your local environment before executing ash tool. There were issues reported with podman, please use docker while we investigate the issue.
