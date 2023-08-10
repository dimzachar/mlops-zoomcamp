[Previous](makefiles_and_hooks.md) | [Next](terraform_modules.md)

# Terraform: Introduction

We will explore how to leverage Terraform to set up infrastructure for a stream-based pipeline in AWS.

## Overview

The objective of this tutorial is to establish a dual-sided Kinesis stream, one for the producer and another for the consumer. We will also set up a Lambda function to serve as our prediction service and an S3 bucket to house our model artifacts. In addition, we will create an ECR repository to store the Docker image for the Lambda container. To round off our setup, we will configure a CloudWatch event that activates our Lambda function when a specific event is detected in the Kinesis stream.

## Prerequisites and Setup

Before we begin, ensure that you have the AWS client installed. You can check the installed version with the command `aws --version`. You will also need to configure your AWS secret key. If you haven't done this already, you can find the key in the IAM section of your AWS console. Once you have the key, you can configure it on your local machine using the command `aws configure`.

## Terraform Basics

If you're new to Terraform, you may want to familiarize yourself with the basic structure of a Terraform project and how to run basic commands like `terraform init`, `plan`, and `apply`. You can find a basic introduction to these topics in the [Data Engineering Zoom Camp](https://github.com/DataTalksClub/data-engineering-zoomcamp). Useful resources:

- [Summary material](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/06-best-practices/docs.md)
- [Terraform overview](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/1_terraform_overview.md) 

## Setting Up the Infrastructure

In this section, we will set up the stream-based pipeline infrastructure in AWS using Terraform. We will cover advanced Terraform concepts like modules and output variables. We will build the components for ECR, Kinesis, Lambda, and S3 as per our architecture needs.

## Deployment and Testing

After setting up the infrastructure, we will manually deploy it and test it locally. In the next section, we will automate all these steps, including the tests, into our CI/CD pipeline.

## Downloading Terraform

You can download the Terraform client from the [official Terraform website](https://www.terraform.io/downloads.html) based on your OS or package manager.

Stay tuned for the next video where we will discuss CI/CD pipelines.


[Previous](makefiles_and_hooks.md) | [Next](terraform_modules.md)