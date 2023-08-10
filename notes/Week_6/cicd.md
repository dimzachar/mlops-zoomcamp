# CI/CD Introduction

In the world of DevOps, Continuous Integration (CI) and Continuous Delivery (CD) play a pivotal role in ensuring that software applications are developed, tested, packaged, and delivered in a structured and efficient manner.

## Overview

CI/CD is a crucial DevOps practice that aids in shortening the delivery time of software applications.

- **CI**: This involves developing, testing, and packaging code in a structured manner.
- **CD**: This is responsible for delivering the integrated code to various dependent applications.

For our use case, we will be implementing a complete CI/CD pipeline using GitHub Actions. This pipeline will automatically trigger jobs to build, test, and deploy our service for every new commit or code change to our repository.

## CI/CD Pipeline Architecture

The architecture represents a full-fledged CI/CD pipeline:

- **GitHub Actions**: It will automatically trigger jobs to build, test, and deploy our service for every new commit or code change to our repository.
- **Goal**: The main objective of our CI/CD pipeline is to execute tests, define our infrastructure, build and push a container image for our service to a specific repository, and update the task definition for our Lambda.

### CI Workflow

This workflow will have two jobs and will be triggered when a pull request is created from a feature branch for our new commits to the repo. It will:

- Auto-test our inference service both locally and on the cloud.
- Run Terraform plan on our specified Terraform state file to compile and validate any infrastructure changes.

### CD Workflow

This workflow will have one job with a series of steps and will be triggered only when a pull request is approved and merged to the main or a developed branch. It consists of:

- **Defining the Infrastructure using Terraform**: This will repeat the steps from our previous section and automate the tf apply step to auto-generate the infrastructure if the tf plan detects any changes.
- **Build and Push**: This will build the Docker image for our Lambda service and then push it to our ECR repository.
- **Deploy**: Once a new version of our Lambda function is published, the deploy step will update the Lambda config to run across multiple environments such as dev, stage, and prod with the environment variables we currently provide.

## Setting up the CI/CD Pipeline

GitHub Actions is our chosen tool for setting up our CI/CD pipeline, offering standardized VMs to run our jobs without manual infrastructure handling.

📁 GitHub Folder Structure

- **.github**: Essential folder for GitHub's CI/CD configurations.

## 🔁 CI Workflow (`workflows/ci-tests.yml`)

This workflow is primarily concerned with testing new code integrations.

**Trigger** 

The workflow is initiated when a pull request is created from any feature branch, targeting the 'develop' branch.

- **Environment**: Configure AWS variables using GitHub Secrets.

```yaml
env:
  AWS_DEFAULT_REGION: 'eu-west-1'
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

- **Jobs Within CI**:

Define the jobs for the workflow. This will include auto-testing our inference service both locally and on the cloud and running Terraform plan on our specified Terraform state file. These jobs can run sequentially or in parallel, based on the needs.

**Job: Test** 

  - Sets up the required environment, checks out the code, run unit tests, and linting to ensure code quality.

```yaml

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        working-directory: "06-best-practices/code"
        run: pip install pipenv && pipenv install --dev

      - name: Run Unit tests
        working-directory: "06-best-practices/code"
        run: pipenv run pytest tests/

      - name: Lint
        working-directory: "06-best-practices/code"
        run: pipenv run pylint --recursive=y .

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ env.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ env.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_DEFAULT_REGION }}

      - name: Integration Test
        working-directory: '06-best-practices/code/integraton-test'
        run: |
          . run.sh
```


**Job: Terraform Plan** 

  - Initialize Terraform state and track infrastructure changes.

```yaml

tf-plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ env.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ env.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_DEFAULT_REGION }}

      - uses: hashicorp/setup-terraform@v2

      - name: TF plan
        id: plan
        working-directory: '06-best-practices/code/infrastructure'
        run: |
          terraform init -backend-config="key=mlops-zoomcamp-prod.tfstate" --reconfigure && terraform plan --var-file vars/prod.tfvars
```

⚙️ Two jobs are defined in the CI pipeline: 'test' and 'TF plan'.
🖥️ The 'runs on' tag specifies the type of machine on which the job will run. 
⏭️ In GitHub Actions, by default, all jobs in a workflow run in parallel. This means that unless specified otherwise, jobs will start executing simultaneously, independent of each other. This is why `- uses: actions/checkout@v2` is required for each job, as each job runs in a new VM and needs its own copy of the code to work with.


## 🚀 CD Workflow (`workflows/cd-deploy.yml`)

This workflow is responsible for deploying the infrastructure changes once they've been approved and merged.

**Trigger**: Activated by pushes to the 'develop' branch.

**Jobs Within CD** 

For the CD workflow, the primary job encompasses building, pushing, and deploying changes. Unlike the CI pipeline, where jobs can run in parallel, the steps in the CD pipeline are interdependent and therefore must execute sequentially to ensure successful deployment.


- **Docker & ECR**: Build, tag, and push Docker image to Amazon ECR.
- **Model Artifacts**: Demonstrate retrieval of the latest model version.

```yaml

jobs:
  build-push-deploy:
    ...
```

The sequence in the CD workflow ensures:

- Infrastructure is defined and changes are applied using Terraform.
- Docker images are built, tagged, and pushed to Amazon ECR.
- Model artifacts are retrieved and applied.
- The AWS Lambda function is updated with the latest configurations.


This step-by-step progression guarantees that each part of the deployment is in place before the next begins, ensuring a smooth and error-free delivery process.

## 🧪 Testing the Pipeline

- **Push Changes**: After making the necessary changes, push them to the repository. Since changes were made in the code directory, the CI pipeline will be triggered. Wait for the CI tests to complete before proceeding.

- **Merge Pull Request**: Once the CI tests are successful, merge the pull request to the 'develop' branch. This action will trigger the Continuous Delivery (CD) pipeline.

- **Observe CD Workflow**: The CD workflow will initiate the Terraform plan, push a new image to the ECR registry, update the model artifacts, and finally update the Lambda service. Once the CD workflow completes successfully, the production Lambda will be updated with the latest changes.

- **Verify Resources**: Navigate to the AWS console and verify the resources. In the state bucket, there should now be two Terraform state files - one for staging and one for production. If you've retained the staging environment, you'll see resources specific to both staging and production.

- **Test the Production Environment**: Just like with the staging environment, you can test the production environment by pushing a record into the production resources and observing the results.

# Conclusion

We learned how to use GitHub Actions to create workflows that automatically test pull requests, build and push Docker images, and deploy updated services to production. By creating specific YAML files in the GitHub repository, a series of automation steps can be automatically triggered.

The power of CI/CD is evident in how it streamlines the development and deployment process. With the knowledge gained, you can further automate tasks with GitHub Actions, such as orchestrating a continuous training pipeline or integrating with a model registry like MLflow or DVC.

Automation not only improves efficiency but also ensures that the latest changes are always deployed in a structured and systematic manner. Whether you're looking to retrain models, fetch the latest model versions, or any other task, automation with GitHub Actions can be a game-changer.


[Previous](terraform_e2e.md)