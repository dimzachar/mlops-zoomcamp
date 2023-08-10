# Terraform: Build an e2e workflow for ride predictions

We continue the process of setting up a pipeline for AWS using Terraform. Previously, we created two Kinesis streams. 

We demonstrate how to set up the rest of the pipeline for ride predictions using Terraform, including configuring S3 for model storage, ECR (Elastic Container Registry) for Docker image storage, and Lambda for model prediction.

## Setup

### Environment-specific variable values

Create a new directory to store variables or resources for different environments (e.g., production, staging). The vars directory contains two files: `prod.tfvars` and `stg.tfvars`. These files define environment-specific values for the variables declared in `variables.tf`. The `prod.tfvars` file contains the variables that are specific to the production environment and `stg.tfvars` the variables that are specific to the staging environment.

```bash
mkdir vars
touch prod.tfvars stg.tfvars
```

When you run Terraform commands, you can specify which variable file to use with the -var-file option, like so:

```bash
terraform plan -var-file="vars/prod.tfvars"
terraform apply -var-file="vars/prod.tfvars"
```

Similarly, replace with "vars/stg.tfvars" to set up the infrastructure for the staging environment.

### S3 module

The S3 module (`modules/s3`) is a reusable Terraform module responsible for creating an Amazon S3 bucket. The `main.tf` file within this module is responsible for creating the S3 bucket:


```hcl
resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.bucket_name
  acl    = "private"
  force_destroy = true
}

output "name" {
  value = aws_s3_bucket.s3_bucket.bucket
}
```

The `aws_s3_bucket` block creates an S3 bucket with the name provided via the `bucket_name` variable. The access control list (ACL) for the bucket is set to "private", meaning the bucket isn't publicly accessible. The `force_destroy` attribute, when set to true, allows Terraform to delete the S3 bucket even if it contains objects. The `output` block exports the name of the bucket, which can be used in other parts of the Terraform configuration.

The `variables.tf` file within the S3 module declares the variable `bucket_name`:

```hcl
variable "bucket_name" {
  description = "Name of the bucket"
}
```

This variable is used to provide a custom name for the S3 bucket. The value for this variable will be supplied when calling the module.


**Main Configuration (`main.tf` and `variables.tf`)**

The main Terraform configuration files (`main.tf` and `variables.tf`) located outside the `modules` directory are responsible for orchestrating the creation of all resources and modules.

In the `main.tf` file, the S3 module is called:

```hcl
# model bucket
module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket}-${var.project_id}"
}
```

Here, `module "s3_bucket"` creates an instance of the S3 module. The `source` attribute tells Terraform where to find the module. The `bucket_name` attribute sets the name of the S3 bucket by combining the `model_bucket` and `project_id` variables with a hyphen.

In the `variables.tf` file, the variable `model_bucket` is declared:

```hcl
variable "model_bucket" {
  description = "s3_bucket"
}
```

This variable is used to provide a part of the custom name for the S3 bucket when calling the S3 module in the `main.tf` file.

### ECR Module (`modules/ecr/main.tf` and `modules/ecr/variables.tf`)

The ECR (Elastic Container Registry) module is used to create an Amazon ECR repository and build and push a Docker image to it.

#### `modules/ecr/main.tf`

The `main.tf` file within this module contains the main configuration:

```hcl
resource "aws_ecr_repository" "repo" {
  name                 = var.ecr_repo_name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = false
  }
  force_delete = true
}
```

The `aws_ecr_repository` block creates an ECR repository with the name provided via the `ecr_repo_name` variable. `image_tag_mutability` is set to "MUTABLE", which means that you can overwrite image tags in this repository. The `force_delete` attribute, when set to true, allows Terraform to delete the ECR repository even if it contains images.

```hcl
resource null_resource ecr_image {
   triggers = {
     python_file = md5(file(var.lambda_function_local_path))
     docker_file = md5(file(var.docker_image_local_path))
   }
   provisioner "local-exec" {
     command = <<EOF
             aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com
             cd ../
             docker build -t ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag} .
             docker push ${aws_ecr_repository.repo.repository_url}:${var.ecr_image_tag}
         EOF
   }
}
```

The `null_resource` block named `ecr_image` triggers a local provisioner to build and push a Docker image to the ECR repository when the hash of the Python or Docker file changes. The `triggers` attribute is used to rebuild the image when the Python or Docker files change. The "local-exec" `provisioner` block executes a series of shell commands to log in to the ECR registry, build the Docker image, and push the image to the ECR repository.

```hcl
data aws_ecr_image lambda_image {
 depends_on = [
   null_resource.ecr_image
 ]
 repository_name = var.ecr_repo_name
 image_tag       = var.ecr_image_tag
}
```

The `aws_ecr_image` data source allows Terraform to use data from an existing image in the ECR repository. It basically fetches the details of the Docker image that's been pushed to the ECR repository. The `depends_on` attribute ensures that this block is only executed after the `null_resource.ecr_image` block has been executed, ensuring that the image is pushed to the ECR repository before its details are fetched.

```hcl
output "image_uri" {
  value     = "${aws_ecr_repository.repo.repository_url}:${data.aws_ecr_image.lambda_image.image_tag}"
}
```

The `output` block exports the URI of the Docker image that's been pushed to the ECR repository. This URI can be used in other parts of the Terraform configuration.

#### `modules/ecr/variables.tf`

The `variables.tf` file within the ECR module declares several variables that are used in the module's configuration:

```hcl
variable "ecr_repo_name" {
    type        = string
    description = "ECR repo name"
}

variable "ecr_image_tag" {
    type        = string
    description = "ECR repo name"
    default = "latest"
}

variable "lambda_function_local_path" {
    type        = string
    description = "Local path to lambda function / python file"
}

variable "docker_image_local_path" {
    type        = string
    description = "Local path to Dockerfile"
}

variable "region" {
    type        = string
    description = "region"
    default = "eu-west-1"
}

variable "account_id" {
}
```

Each variable is declared with a name, and it can include a description, type, and default value. Variables make the Terraform configuration more flexible and reusable.

**Main Configuration (`main.tf` and `variables.tf`)**

In the main Terraform configuration files (`main.tf` and `variables.tf`) located outside the `modules` directory, the ECR module is called:

```hcl
module "ecr_image" {
   source = "./modules/ecr"
   ecr_repo_name = "${var.ecr_repo_name}_${var.project_id}"
   account_id = local.account_id
   lambda_function_local_path = var.lambda_function_local_path
   docker_image_local_path = var.docker_image_local_path
}
```

Here, `module "ecr_image"` creates an instance of the ECR module. The `source` attribute tells Terraform where to find the module. Other attributes set specific variables for the module, including the name of the ECR repository, the AWS account ID, and the local paths to the Lambda function Python file and the Dockerfile.


In the `variables.tf` file, the variables are used to provide values to the ECR module when it's called in the main main.tf file. 


```hcl
variable "lambda_function_local_path" {
  description = ""
}
```

This variable is used to specify the local file path to the Python file that contains the AWS Lambda function code. This is particularly important in the ECR module, as the `null_resource` block uses this path to trigger a Docker image rebuild when the Python file changes.

```hcl
variable "docker_image_local_path" {
  description = ""
}
```

This variable is used to specify the local file path to the Dockerfile. This Dockerfile contains instructions on how to build the Docker image that is used by the AWS Lambda function. This variable is also used in the `null_resource` block in the ECR module to trigger a Docker image rebuild when the Dockerfile changes.


```hcl
variable "ecr_repo_name" {
  description = ""
}
```

This variable is used to provide a custom name for the ECR repository that is created in the ECR module. 


### Lambda Module (`modules/lambda`)

The Lambda module defines an AWS Lambda function and an IAM role with the necessary permissions for the function. The `main.tf` file creates the Lambda function, the `variables.tf` file declares any necessary variables and `iam.tf` the IAM role resources.

### `main.tf`

In your main.tf file, define the AWS Lambda function. The function requires a name and a package type, which could be either a zip file or a Docker image. If you're using a Docker image, you'll need to provide the image URI, which is the location of the Docker image on the cloud. The function also has a role that allows it to execute and interact with Kinesis, sets up its event invoke configuration, and maps the Lambda function to the source Kinesis data stream.

#### `aws_lambda_function` block

This block creates the AWS Lambda function:

```hcl
resource "aws_lambda_function" "kinesis_lambda" {
  function_name = var.lambda_function_name
  image_uri = var.image_uri   # required-argument
  package_type = "Image"
  role          = aws_iam_role.iam_lambda.arn
  tracing_config {
    mode = "Active"
  }
  environment {
    variables = {
      PREDICTIONS_STREAM_NAME = var.output_stream_name
      MODEL_BUCKET = var.model_bucket
    }
  }
  timeout = 180
}
```

#### `aws_lambda_function_event_invoke_config` block

This block configures the event invoke configuration for the Lambda function:

```hcl
resource "aws_lambda_function_event_invoke_config" "kinesis_lambda_event" {
  function_name                = aws_lambda_function.kinesis_lambda.function_name
  maximum_event_age_in_seconds = 60
  maximum_retry_attempts       = 0
}
```

The `maximum_event_age_in_seconds` attribute sets the maximum age of a request that Lambda sends to a function for processing. The `maximum_retry_attempts` attribute sets the maximum number of times to retry when the function returns an error.

#### `aws_lambda_event_source_mapping` block

This block maps the Lambda function to the source Kinesis data stream:

```hcl
resource "aws_lambda_event_source_mapping" "kinesis_mapping" {
  event_source_arn  = var.source_stream_arn
  function_name     = aws_lambda_function.kinesis_lambda.arn
  starting_position = "LATEST"
  depends_on = [
    aws_iam_role_policy_attachment.kinesis_processing
  ]
}
```

The `depends_on` attribute ensures that this block is only executed after the `aws_iam_role_policy_attachment.kinesis_processing` block has been executed.

### `variables.tf`

This file declares the variables used in `main.tf`. The variables include the names and ARNs of the source and output Kinesis data streams, the name of the model bucket, the name of the Lambda function, and the URI of the Docker image in the ECR repository.

### `iam.tf`

This file sets up the IAM roles and policies that the Lambda function needs to access the Kinesis data streams, write logs to CloudWatch, and access the model bucket in S3.


**Main Configuration (`main.tf` and `variables.tf`)**

The `module` block for `lambda_function` is where we're using the Lambda module:

```hcl
module "lambda_function" {
  source = "./modules/lambda"
  image_uri = module.ecr_image.image_uri
  lambda_function_name = "${var.lambda_function_name}_${var.project_id}"
  model_bucket = module.s3_bucket.name
  output_stream_name = "${var.output_stream_name}-${var.project_id}"
  output_stream_arn = module.output_kinesis_stream.stream_arn
  source_stream_name = "${var.source_stream_name}-${var.project_id}"
  source_stream_arn = module.source_kinesis_stream.stream_arn
}
```

In the `variables.tf` file in the base configuration folder, you have defined the `lambda_function_name` variable:

```hcl
variable "lambda_function_name" {
  description = ""
}
```

## Trigger event

### Overview

We learnt how to deploy a full pipeline on AWS with Terraform. Our pipeline's core function is to seamlessly respond to new ride events in a Kinesis stream. Once a new event is detected, an AWS Lambda function is activated. This function, equipped with the capability to fetch specific machine learning model versions from an S3 bucket, proceeds to generate insightful predictions. These predictions are then efficiently relayed to an output Kinesis stream. As we guide you through each step to achieve this streamlined process, we'll also demonstrate how to test the setup by inserting an event into the source Kinesis stream and validating that the expected output is correctly received.


## Configuring Lambda Environment

Before we dive into testing, it's essential to equip the Lambda function with the necessary context. These environment variables act as pointers, guiding the Lambda function to the necessary resources:

  - **PREDICTIONS_STREAM_NAME**: Directs the Lambda to the output Kinesis stream.
  - **MODEL_BUCKET**: Points to the S3 bucket for model fetching. It ensures the Lambda function fetches the correct model artifacts for predictions. 
  - **RUN_ID**: Ensures the Lambda uses the correct model version. The Run ID typically corresponds to a hash ID of the current version of the model and can be found in the "mlflow models" bucket.

For efficient data processing, set up the Kinesis streams:

```hcl
export KINESIS_STREAM_INPUT="stg_ride_events-mlops-zoomcamp"
export KINESIS_STREAM_OUTPUT="stg_ride_predictions-mlops-zoomcamp"
```

## Fetching the Model Version (Run ID)

Understanding which version of the model to use is crucial. In a production environment, the training pipeline would typically update the Run ID in the model registry. However, for this exercise, we'll use a manual method to fetch the most recent model partition. The `deploy_manual.sh` script retrieves the latest model version, ensuring that the Lambda function always uses the most recent and optimal model for its predictions.

```hcl
export RUN_ID=$(aws s3api list-objects-v2 --bucket ${MODEL_BUCKET_DEV} --query 'sort_by(Contents, &LastModified)[-1].Key' --output=text | cut -f2 -d/)
```

Following this, synchronize the model artifacts between the development and production buckets, ensuring a consistent environment:

```hcl
aws s3 sync s3://${MODEL_BUCKET_DEV} s3://${MODEL_BUCKET_PROD}
```

## Updating the Lambda Function

With the environment variables in place, update the Lambda function context so it's aware of data sources and destinations.

```hcl
variables="{PREDICTIONS_STREAM_NAME=${PREDICTIONS_STREAM_NAME}, MODEL_BUCKET=${MODEL_BUCKET_PROD}, RUN_ID=${RUN_ID}}"
aws lambda update-function-configuration --function-name ${LAMBDA_FUNCTION} --environment "Variables=${variables}"
```

## Testing with Kinesis

Simulate a real-world scenario by pushing a ride event to the Kinesis input stream. This emulates live operations:

```bash
SHARD_ID=$(aws kinesis put-record  \
        --stream-name ${KINESIS_STREAM_INPUT}   \
        --partition-key 1  --cli-binary-format raw-in-base64-out  \
        --data '{"ride": {
            "PULocationID": 130,
            "DOLocationID": 205,
            "trip_distance": 3.66
        },
        "ride_id": 156}'  \
        --query 'ShardId'
    )
```

## Verifying the Lambda Execution

After triggering the Lambda, it's crucial to dive into AWS CloudWatch logs to ensure predictions are generated and processed correctly.

## Closing Notes

**Benefits of Infrastructure as Code (IaC)**:

- **Version Control** : Keep track of changes, easily roll back, or replicate setups. 
- **Environment Duplication** : Whether it's testing, staging, or production, IaC ensures all environments mirror each other. 
- **Cloud Provider Agnostic** : Tools like Terraform support multiple cloud providers, making migrations or multi-cloud deployments easier.

**What's Next**:

- Future tutorials will focus on automating the deployment process using CI/CD with GitHub Actions. This will further streamline deployments, making them faster and more reliable.

**Stay tuned as we delve deeper into the world of cloud infrastructure automation!**

[Previous](terraform_modules.md) | [Next](cicd.md)
