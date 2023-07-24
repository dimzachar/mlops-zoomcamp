# Best Engineering Practices: Unit Tests, Integration Tests, and AWS Services

## Introduction

Welcome back to session 6 of our #mlopszoomcamp. In this session, we delve into the best engineering practices, focusing on unit tests, integration tests, and the use of LocalStack for AWS services.

We will take the example we built in Module 4, a simple architecture involving two Kinesis streams, a Lambda function, and an S3 bucket, and improve it from an engineering perspective.  The system is set up in a way that it can receive a stream of incoming ride data, make predictions on that data, and then send those predictions to another Kinesis stream for further processing.

![architecture](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_6/Images/architecture.svg)

# Adding Unit Tests to Your Python Project: A Tutorial Using Visual Studio Code and pytest

We'll cover setting up the environment, creating unit tests, and refactoring code for better testability.

## Set Up Your Environment

First, we need to set up our environment. We'll create a new folder for our project and copy the code from Module 4 we want to test into it.

```bash
pipenv install
```

## Install pytest

We will use Pytest for creating tests, which will be stored in a separate tests folder. You can install it on a dev environment:

```bash
pipenv install --dev pytest
pipenv shell
```

Make sure you have a Python interpreter installed and selected for your project.

## Write Your First Test

Now you're ready to write your first test. We'll create a new directory named "tests" in our project folder and a new Python file for our tests.

```bash
mkdir tests
cd tests
touch model_test.py
touch __init__.py
```

Start with just 
```python
assert 1 == 1
```
on your `model_test.py` to check if it works.

Step 4: Run Your Test
You can run your test directly from Visual Studio Code by clicking on the "Run Test" link, or run

```bash
pipenv run pytest tests/
```

This command will automatically discover and run all tests in your project.

## Write Unit Tests and Refactor Code

Now that you know how to write and run a test, you can start writing more tests for your project. Unit tests are typically used to test functions. As you write tests, you might find that some parts of your code are hard to test. This is usually a sign that you need to refactor your code. Try to make your code more modular and avoid global state to make it easier to test.

We will refactor our code from `lambda_function.py` by creating a new class called `ModelService` on a new file `model.py`. This class wraps around the machine learning model and provides methods for preparing the features for the model and predicting the ride duration. It contains all the logic of our Lambda function, meaning it provides a handler for AWS Lambda functions to process a batch of ride events from a Kinesis stream.

The ModelService class will have the following methods:

- __init__()`: This method will initialize the class with the necessary parameters.
- prepare_features()`: This method will prepare the features for our model.
- predict()`: This method will make predictions using our model.
- lambda_handler()`: This method will handle the Lambda function invocation.

We also make use of `callbacks` that provides flexibility and modularity. `Callbacks` are used to allow custom behavior to be injected into the `ModelService` class. This allows the `ModelService` class to remain decoupled from the specifics of what happens after a prediction is made. One of the `callback` functions provided is the `put_record` method of the `KinesisCallback` class. This method puts the prediction event into a Kinesis stream.

We can write now unit tests for each method in the `ModelService` class on `model_test.py`:

- `test_prepare_features()`: This test checks the `prepare_features` method, which takes in ride data and returns a set of features, of the `ModelService` class. It creates a `ModelService` object, prepares the features for a ride, and checks if the result is as expected.

- `test_base64_decode()`: This test checks the `base64_decode` function. It reads the base64 encoded data from a file, decodes it using the function, and checks if the result is as expected.

- `test_predict()`: This test checks the predict method of the `ModelService` class. It creates a `ModelService` object with a ModelMock object, predicts the ride duration for some features, and checks if the result is as expected.

- `test_lambda_handler()`: This test checks the `lambda_handler` method of the `ModelService` class. It creates a `ModelService` object with a `ModelMock` object, handles a Lambda function event, and checks if the result is as expected.

The tests use the `assert` statement to check if the actual results are equal to the expected results. If a test fails, the `assert` statement will raise an `AssertionError` exception.

## Run All Tests
Once you've written tests for all functions in your project, you can run all tests to make sure everything works correctly. Again, you can do this directly from Visual Studio Code or from the command line using the pytest command.

That's it! You now know how to add unit tests to your Python project using pytest and Visual Studio Code. Happy testing!


# Integration Tests

In addition to unit tests, which test individual parts of our code, we should write integration tests that test our code as a whole.
We will use the `test_docker` script to run these tests.


## Prerequisites
Before we begin, make sure you have the following installed:

- Docker
- Docker Compose

## Building and Running the Docker Image

Next, we will build a Docker image for our application. Navigate to the directory containing your Dockerfile and run the following command:

```bash
docker build -t stream-model-duration:v2 .
```

After the image is built, we can run a container from this image using the following command:\

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```

The -e options set environment variables in the container.

## Writing and Running Tests

In module 4 the `test_docker` script was used to send some pre-defined data to a server, then prints out the server's response. 
We refactor it by loading the event data from a JSON file instead of having it directly in the code and write tests for our application to ensure that a service (a machine learning model's prediction endpoint) is returning the expected results. We do this by comparing the actual response of the service with an expected response. 

### Comparing Dictionaries

We use the DeepDiff function from the deepdiff library, which is used to compare two Python dictionaries and identify where they differ. We install it

```bash
pipenv install --dev deepdiff
```

and on our script we have

```python
diff = DeepDiff(actual_response, expected_response, significant_digits=1)
print(f'diff={diff}')
```

If there are any differences, they will be printed out. When comparing floats, as they often have long decimal places due to floating-point arithmetic in Python, we allow for tolerance by using the `significant_digits=1` argument from DeepDiff to consider numbers as the same if they match up to the first decimal place.
Finally, the script checks to make sure that there are no differences in the type or value of data between the actual and expected responses. If there are, the script will stop executing and raise an `AssertionError`. This is the final check to ensure that the server's output matches our expectations.

```python
assert 'type_changes' not in diff
assert 'values_changed' not in diff
```

### Removing Dependency on S3

We discuss how to remove the test's dependency on S3 by downloading the model and storing it locally to  use it in the tests. We introduce the use of environment variables to configure the bucket and experiment ID and also provide a way to define the whole path to the model. If the model location is set, it will return it; otherwise, it will build the path as it did previously.

To make the model available to the Docker container, we can mount a directory from the host machine to the container. We can do this using the `-v` option in the `docker run` command:

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    -v $(pwd)/model:/app/model \
    stream-model-duration:v2
```

The `-v $(pwd)/model:/app/model` option mounts the `model` directory from the current directory on the host machine to the `/app/model` directory in the Docker container.

We can run the test using the following command:

```bash
cd integration-test
pipenv run python test_docker.py
```

# LocalStack for AWS Services

However, we didn't test the Kinesis connection or the function that puts the responses to the Kinesis stream. 
This is where LocalStack comes into play. Specifically, we will focus on testing the Kinesis connection and the function that puts responses into the Kinesis stream.

## Setting Up LocalStack

LocalStack is a powerful tool that provides a fully functional local AWS cloud stack, making it ideal for testing AWS services locally. To use LocalStack, we first need to install it. We can do this using Docker Compose and specifying the services we want to run. For our purposes, we only need to run the Kinesis service.

Here is an example of a Docker Compose file that sets up LocalStack:

```yaml
services:
  backend:
    image: ${LOCAL_IMAGE_NAME}
    ports:
      - "8080:8080"
    environment:
      - PREDICTIONS_STREAM_NAME=${PREDICTIONS_STREAM_NAME}
      - RUN_ID=Test123
      - AWS_DEFAULT_REGION=eu-west-1
      - MODEL_LOCATION=/app/model
      - KINESIS_ENDPOINT_URL=http://kinesis:4566/
      - AWS_ACCESS_KEY_ID=abc
      - AWS_SECRET_ACCESS_KEY=xyz
    volumes:
      - "./model:/app/model"
  kinesis:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=kinesis
```

Once LocalStack is installed, we can create a Kinesis stream within it. This will allow us to test our Kinesis connection.

## Configuring the Code to Access LocalStack

With our Kinesis stream set up in LocalStack, we need to configure our code to access the local endpoint instead of the AWS endpoint. We can do this by creating a function that creates a Kinesis client and sets the endpoint URL to our local endpoint if it is set.

Here is an example of how to create a Kinesis client that connects to LocalStack:

```python
def create_kinesis_client():
    endpoint_url = os.getenv('KINESIS_ENDPOINT_URL')

    if endpoint_url is None:
        return boto3.client('kinesis')

    return boto3.client('kinesis', endpoint_url=endpoint_url)
```

## Testing the Kinesis Connection

Now that our code is configured to access the local endpoint, we can test the Kinesis connection. We can use the AWS CLI to list the streams in our local Kinesis service. After creating a stream, we can check that it is present in LocalStack but not in our AWS account.

## Running the Integration Test

With our Kinesis connection tested, we can run our integration test. This test sends a request to the service and writes something to the Kinesis stream. We can then access the Kinesis stream to ensure that the expected data was written.

The integration test involves several steps:

1. **Setting Up the Environment**: We specify the Kinesis endpoint, the stream name, and the shard ID to set up our testing environment.

2. **Acquiring the Shard Iterator**: We use the `get_shard_iterator` method to acquire a shard iterator, which is a pointer to a specific point in a shard.

3. **Retrieving Records**: With the shard iterator, we retrieve records from the stream using the `get_records` method.

4. **Verifying the Data**: We verify the retrieved data by comparing it to the expected data. We use the `DeepDiff` library to check for any significant differences between the actual and expected data.

By following these steps, you can effectively test your AWS services locally using LocalStack. This can greatly streamline your development process and ensure that your services are functioning as expected before deploying them to AWS.


## Automating the Process

Basically, we want to automate the process of building the Docker image, run a Docker Compose setup, create a Kinesis stream, run some Python tests, and clean up the setup.

We create a script `run.sh`, make sure to make it executable and run it with
```bash
chmod +x integration_test/run.sh
./run.sh
```

Let's break down the script:

**Step 1: Change the current directory**

```bash
if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi
```

If the `GITHUB_ACTIONS` environment variable is not set (which means the script is not being run by GitHub Actions), the script changes the current working directory to the directory where the script is located.

**Step 2: Build a Docker image if necessary**

```bash
if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
    echo "LOCAL_IMAGE_NAME is not set, building a new image with tag ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "no need to build image ${LOCAL_IMAGE_NAME}"
fi
```

If the `LOCAL_IMAGE_NAME` environment variable is not set, the script builds a new Docker image. Here we augment the image with additional information to make version tracking more informative and manageable. So it creates a tag for the image using the current date and time, then uses the `docker build` command to build the image using the Dockerfile in the parent directory (`..`). If `LOCAL_IMAGE_NAME` is already set, it skips this step.

**Step 3: Set up Docker Compose and a Kinesis stream**

```bash
export PREDICTIONS_STREAM_NAME="ride_predictions"

docker-compose up -d

sleep 5

aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --shard-count 1
```

The script sets up a Docker Compose environment in detached mode (`-d`), waits for 5 seconds to ensure everything is up and running, then uses the AWS CLI to create a Kinesis stream named "ride_predictions" with 1 shard.

**Step 4: Run Python tests**

```bash
pipenv run python test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

pipenv run python test_kinesis.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi
```

The script runs two Python tests (`test_docker.py` and `test_kinesis.py`) using Pipenv. After each test, it checks whether the test was successful by examining the exit code. If the exit code is not 0 (which indicates an error), the script prints the Docker Compose logs, shuts down the Docker Compose setup, and exits with the error code.

**Step 5: Clean up**

```bash
docker-compose down
```

Finally, the script shuts down the Docker Compose setup. This happens regardless of whether the tests were successful. 
So, in summary, this script is a testing pipeline that builds an image, sets up a Docker Compose environment, runs tests against it, and cleans up the environment afterward. It's a good example of how you can automate testing for a Dockerized application.

# Next

In the next video, we will cover code quality checks, automatic code formatting, and the use of make files for running tests.
By following these steps, we can ensure that our Python code is thoroughly tested and works as expected. Remember to commit your code and your tests to GitHub regularly. This way, others can see your tests and how your code is supposed to work. Plus, if your project is open source, other contributors can run your tests to make sure their changes don't break anything.

[Next](code_quality.md)