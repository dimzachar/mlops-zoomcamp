# MLOps Notes

## Chapter 1: Introduction to ML Experiments and MLflow

MLflow is an open-source platform used to manage the Machine Learning (ML) lifecycle, including experimentation, reproducibility, deployment, and a central model registry. It's a Python package with four main modules: Tracking, Models, Model registry, and Projects.

In the context of ML, an experiment is the process of building an ML model. An experiment run is each trial in an ML experiment, and any file associated with an ML run is called a run artifact. Examples of run artifacts include the model itself, package versions, and others. Metadata tied to each experiment is referred to as experiment metadata.

Experiment tracking is the process of keeping track of all the relevant information from an ML experiment. This helps with reproducibility, organization, and optimization. Traditional methods such as spreadsheets fall short in key points, so MLflow is typically used for this purpose.

## Chapter 2: Installing and Interacting with MLflow

MLflow can be installed via pip or conda. MLflow has different interfaces, each with their pros and cons. The MLflow UI is introduced as one of the core functionalities of MLflow. To run the MLflow UI locally, the command `mlflow ui --backend-store-uri sqlite:///mlflow.db` is used. In this command, a SQLite backend with the file `mlflow.db` in the current running repository is used as the backend storage, which is essential to access the features of MLflow.

Additionally, an artifact root directory where artifacts for runs are stored can be added using the `--default-artifact-root` parameter.

Another interface that is introduced is the Tracking API, used to automate processes. This is initialized using the `MlflowClient` from `mlflow.tracking` module. This client object allows managing experiments, runs, models, and model registries.

## Chapter 3: Experiment Management with MLflow

Creating a new experiment is done in the top left corner of the UI or using the Python API with `client.create_experiment("experiment-name")`.

To track experiment runs, `mlflow.set_tracking_uri("sqlite:///mlflow.db")` and `mlflow.set_experiment("experiment-name")` are used to set the tracking URI and the current experiment name. If the experiment does not exist, it will be automatically created.

Within a run, data can be logged including tags, parameters, and metrics. There are three types of artifacts that can be logged: local files, directories, or remote file URLs. When a run is done, it needs to be ended with `mlflow.end_run`.

## Chapter 4: Hyperparameter Optimization and Autologging

Hyperparameter optimization can be tracked using MLflow by logging the hyperparameters used and the resulting model performance metrics for each run. This allows for easy comparison of different versions of the model and identification of the best model based on the metrics.

Autologging is a feature of MLflow that, when enabled, automatically captures MLflow entities when running training code. It automatically creates a new run and logs parameters, metrics, and artifacts.



# MLOps Notes

## Objectives
The primary objective is to understand the flow of Experiment tracking and the utilization of MLFlow for registering this tracking.

## Experiment Tracking
Key Concepts:
- **ML experiment**: The process of building an ML model.
- **Experiment run**: Each trial in an ML experiment, involving data manipulation and hyperparameter tuning.
- **Run artifact**: Any file associated with an ML run.
- **Experiment metadata**: Parameters in the experiment, files for training, testing, and validation, and the model name.

Experiment tracking is the process of saving relevant information of the experiment, such as source code, environment, data, model, hyperparameters, and metrics. This is beneficial for version control, reproducibility, organization, and optimization.

## MLFlow
MLFlow is an open-source platform for the ML Lifecycle, offering tracking, model registry, and project management. It organizes experiments and keeps track of parameters, metrics, metadata, artifacts, and models.

## MLFlow Setup
To run MLFlow locally, create a new virtual environment with Python 3 and install MLFlow. 

## Machine Learning Lifecycle
The lifecycle in MLOps includes data sourcing, data labeling, data versioning, model management, model deployment, hardware scaling, and prediction monitoring.

## Model Registry
The Model Registry is essential for implementing new models or making changes to existing models. It allows for easy rollbacks in case of errors or failures.

## MLFlow in Practice
Different scenarios require different setups, from a single data scientist working on a competition model, to cross-functional teams working on a single model, to multiple data scientists working on multiple models.

## Limitations and Alternatives
MLFlow has some limitations, such as lack of user authentication and data versioning. Alternatives include Neptune, Comet, and Weights & Biases.

