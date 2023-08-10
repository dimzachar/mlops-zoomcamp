[Previous](terraform_intro.md) | [Next](terraform_e2e.md)

# Terraform: Modules and Output Variables

## Introduction

In this tutorial, we will learn about Terraform modules and output variables. Modules are the building blocks in Terraform that allow us to create reusable components, enhance organization, and treat infrastructure elements as a black box. This is especially beneficial when you want to prevent repetition across multiple environments such as staging and production.

## Prerequisites

- Terraform installed on your local machine
- Basic knowledge of Terraform and AWS

## Steps

**Create a new folder for Terraform files**

In your project directory, create a new folder named `infrastructure`. The infrastructure directory contains several Terraform files. Create two base Terraform files: `main.tf` and `variables.tf`.

```bash
    mkdir infrastructure
    cd infrastructure
    touch main.tf variables.tf
```

   The `main.tf` file is the primary entrypoint for Terraform, where we define what providers we are going to use, what resources we want to create, and how they are configured. The `variables.tf` file is where we define any input variables that our configuration might require. These files form the basis of any Terraform project and are usually the first files you will create when starting a new project.

The following directories will also be part of the infrastructure:

- modules/: A directory that contains several modules for different AWS services.
- vars/: A directory that contains environment-specific variable files.


**Configure the Terraform block**

    In the `main.tf` file, start with the Terraform block which is used to configure some basic Terraform settings to provision your infrastructure.

```hcl
    terraform {
      required_version = ">= 1.0"
    }
```

    Here, we've used the `required_version` tag to set our Terraform version that we've installed on the local machine. By specifying the `required_version` in the Terraform block, we ensure that our code is compatible with the version of Terraform we are using. This is crucial because different versions of Terraform may have different features and syntax. If we don't specify a version, Terraform will use the latest
version available, which may lead to compatibility issues if our code relies on features or syntax from
an older version.

**Configure the Terraform Backend**

    In the `main.tf` file, configure the backend to store the state of the Terraform configuration. This is used to identify what new resources have been added or existing resources have been modified.

```hcl
    terraform {
      backend "s3" {
        bucket = "tf-state-mlops-zoomcamp"
        key    = "mlops-zoomcamp-stg.tfstate"
        region = "eu-west-1"
	encrypt = true
      }
    }
```

    By configuring the backend, we can store the state remotely, which is beneficial for team collaboration and keeping the state secure. Here, we are explicitly stating that we want to save the state on a remote service such as AWS S3 bucket. We also specify which bucket it should be stored in, what should be the file name of that particular state file (the key), and the AWS region.

    Note: You will need to create the state bucket manually before you run any Terraform commands.

**Configure AWS for Remote State**

    Accessing state in a remote service requires authorization via AWS configuration. We've already done that using the AWS configuration `aws configure` command in the previous step.

    If you use profiles, then please ensure you're basically attaching your profile configuration also along with that.

**Configure AWS Resources with Terraform**

    The next part that we need is the provider block. The provider block is for the cloud provider we're using, in this case, it's AWS. This helps add a set of predefined resource types and data sources from HashiCorp's AWS module that Terraform can manage.

```hcl
    provider "aws" {
      region = var.aws_region
    }
```

    Here, we've configured the AWS region using a variable. We will define this variable in the `variables.tf` file.

**Configure AWS region and project ID variables**

    In the `variables.tf` file, define the AWS region and project ID variables.

```hcl
    variable "aws_region" {
      description = "The region where AWS operations will take place. Examples are us-east-1, us-west-2, etc."
      default     = "eu-west-1"
    }

    variable "project_id" {
      description = "The ID of the project"
      default     = "mlops-zoomcamp"
    }
```

    Here, we've set the default AWS region to `eu-west-1` and the default project ID to `mlops-zoomcamp`. By defining these variables, we can make our Terraform code more flexible and reusable. For example, if we want to deploy our infrastructure in a different AWS region, we can simply change the value of the `aws_region` variable when running our Terraform commands, instead of having to modify our Terraform code. 

**Configure AWS Caller Identity**

    The AWS Caller Identity is a data source that allows you to use identity-based policies for access to Terraform. It returns the account ID, user ID, and ARN of the effective user.

    In the `main.tf` file, add the AWS Caller Identity data source.

```hcl
    data "aws_caller_identity" "current_identity" {}
```

    This block fetches the current identity (account ID, user ID, and ARN) of the caller. This is useful for getting the account ID for the AWS account, which can be used in other resources.

**Create a Local Variable for Account ID**

    In the `main.tf` file, create a local variable for the account ID. Local variables in Terraform are a convenient way to name and manage commonly used values. They are defined using the `locals ` block

```hcl
    locals {
      account_id = data.aws_caller_identity.current_identity.account_id
    }
```

    Here, we've created a local variable `account_id` and assigned it the account ID from the AWS Caller Identity data source. This local variable can be used within the local file, making our code cleaner and easier to understand.


**Create a Modules Directory**

    Now, let's create a modules directory for our custom modules. Modules in Terraform are self-contained packages of Terraform configurations that are managed as a group. Modules are used to create reusable components in Terraform as well as for basic code organization. These modules would be for two Kinesis streams, one on the producer and one on the consumer side, an S3 bucket to store our model artifacts, an ECR registry to store the Docker image of our Lambda and parent service, and a Lambda configuration for the inference or prediction service.

```bash
    mkdir modules
```
    The modules can be reused across different environments (like staging and production), making our infrastructure code more efficient.

**Create a Kinesis Module**

    Within the Kinesis module, create the base Terraform files: `main.tf` and `variables.tf`.

```bash
    cd modules
    mkdir kinesis
    cd kinesis
    touch main.tf variables.tf
```

    In the `main.tf` file of the Kinesis module, create a Kinesis stream configuration.

```hcl
    resource "aws_kinesis_stream" "stream" {
      name             = var.stream_name
      shard_count      = var.shard_count
      retention_period = var.retention_period
      shard_level_metrics = var.shard_level_metrics
      tags = {
        CreatedBy = var.tags
      }
    }
```

    Here, we've created a Kinesis stream with the specified name, shard count, retention period, shard level metrics, and tags. The values for these parameters are defined in the `variables.tf` file. By defining the
configuration parameters as variables, we can customize the Kinesis stream for different use cases or environments by simply providing different values for the variables.

    In the `variables.tf` file, define the variables for the Kinesis stream.

```hcl
    variable "stream_name" {
        type        = string
        description = "Kinesis stream name"
    }

    variable "shard_count" {
        type        = number
        description = "Kinesis stream shard count"
    }

    variable "retention_period" {
        type        = number
        description = "Kinesis stream retention period"
    }

    variable "shard_level_metrics" {
        type        = list(string)
        description = "shard_level_metrics"
        default     = [
        "IncomingBytes",
        "OutgoingBytes",
        "OutgoingRecords",
        "ReadProvisionedThroughputExceeded",
        "WriteProvisionedThroughputExceeded",
        "IncomingRecords",
        "IteratorAgeMilliseconds",
      ]
    }

    variable "tags" {
      description = "Tags for kinesis stream"
        default = "mlops-zoomcamp"
    }
```

    Here, we've defined the variables for the Kinesis stream name, shard count, retention period, shard level metrics, and tags. The `default` attribute provides default values for these variables.


**Define Output for the Kinesis Stream**

    Outputs in Terraform are a way to tell Terraform what data is important. This data is outputted when `apply` is called, and can be queried using the `output` command. In the `main.tf` file, define an output for the ARN of the Kinesis stream.

```hcl
    output "stream_arn" {
      value = aws_kinesis_stream.stream.arn
    }
```

    Basically, outputs are a way to extract information about the resources that have been created. Here, we've defined an output `stream_arn` that will display the ARN of the Kinesis stream once it's created. This is useful for referencing the stream in other resources or modules.


**Create Kinesis Stream Modules**

    In the `main.tf` file, create modules for the source and output Kinesis streams.

```hcl
    # ride_events
    module "source_kinesis_stream" {
      source = "./modules/kinesis"
      retention_period = 48
      shard_count = 2
      stream_name = "${var.source_stream_name}-${var.project_id}"
      tags = var.project_id
    }

    # ride_predictions
    module "output_kinesis_stream" {
      source = "./modules/kinesis"
      retention_period = 48
      shard_count = 2
      stream_name = "${var.output_stream_name}-${var.project_id}"
      tags = var.project_id
    }
```

    Here, we've created two modules: `source_kinesis_stream` and `output_kinesis_stream`. These modules use the Kinesis module we defined earlier and set the retention period, shard count, stream name, and tags for each stream. By creating these modules, we can easily create multiple Kinesis streams with the same configuration. This is particularly useful when we want to create similar resources for different environments or use cases.

    In the `variables.tf` file, define the variables for the source and output stream names.

```hcl
    variable "source_stream_name" {
      description = "The name of the source Kinesis stream"
    }

    variable "output_stream_name" {
      description = "The name of the output Kinesis stream"
    }
```

    Here, we've defined the variables for the source and output Kinesis stream names. These variables will be used in the modules for the Kinesis streams.

**Initialize and Apply the Terraform Configuration**

    First, you need to initialize your Terraform working directory. This is an essential step because it downloads the necessary provider plugins, sets up the backend for storing your state file, and performs several other necessary setups. You can do this using the `terraform init` command.

```bash
    terraform init
```

    The `terraform init` command is safe to run multiple times, to bring the working directory up to date with changes in the configuration. While `init` is most commonly run without any arguments, there are several options available to customize its behavior.

    During initialization, Terraform will generate a `.terraform.lock.hcl` file in the current working directory. This file records the exact provider versions used to ensure that every Terraform run is consistent. It is recommended to commit this file to your version control system to ensure that all team members and your production infrastructure use the same provider versions.

    After your Terraform working directory has been successfully initialized, you can apply your Terraform configuration. The `terraform apply` command is used to apply the changes required to reach the desired state of the configuration, or the pre-determined set of actions generated by a `terraform plan` execution plan.

```bash
    terraform apply
```

    By default, apply scans the current directory for the configuration and applies the changes appropriately. It will prompt you for confirmation before making any changes to your infrastructure.
You'll need to provide the required arguments that haven't been assigned any values yet. In this case, it's the source stream name. Let's call it `ride_events_sdg`.

```bash
    terraform apply -var="source_stream_name=ride_events_sdg"
```

    Once confirmed, it will proceed to create the resources. The `terraform apply` command first displays a "plan" showing what will happen when you apply your configuration. This plan includes any resources that will be created, modified, or destroyed. In this case, it shows that a new Kinesis stream will be created. After verifying the plan, confirm the apply operation. Terraform will then create the infrastructure on your AWS cloud. This includes creating the Kinesis data streams as defined in your configuration.

**Check Created Resources**

    After the `terraform apply` command completes, you can check the created resources in your AWS console. Navigate to the Kinesis section and you should see the data streams that were created.

    You can also use the AWS CLI or SDKs to interact with the Kinesis data streams and verify their creation. For example, you can use the `describe-stream` command to get information about a stream.

```bash
    aws kinesis describe-stream --stream-name your-stream-name
```

    Replace `your-stream-name` with the name of your Kinesis data stream. This command will return a JSON object with information about the stream.

## Conclusion

In this tutorial, we learned about Terraform modules and output variables. We created a reusable component using Terraform modules and used output variables to display the ARN of AWS Kinesis Stream. We also learned how to configure the Terraform backend, AWS for remote state, and AWS resources with Terraform.

For more information, you can check out the [official Terraform documentation](https://www.terraform.io/docs/language/modules/develop/index.html).

Congratulations! You've now learned how to use Terraform at a basic level, create a custom module, and provision it on your AWS cloud. In the next part we'll code the entire pipeline end-to-end.

[Previous](terraform_intro.md) | [Next](terraform_e2e.md)