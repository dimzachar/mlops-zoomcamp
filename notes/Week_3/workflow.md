# Chapter 3: Productionizing a Jupyter Notebook into a Python Script using Prefect


The third chapter takes a comprehensive look at the process of converting a Jupyter notebook into a Python script with Prefect. It examines the data pipeline, including the data read-in, feature engineering, and model training process, and integrates these steps into a Prefect flow. Detailed tutorials demonstrate adding orchestration and observability to ML workflows, utilizing Prefect features like caching and decorators.

## Hands-On with Prefect 2.0

In Prefect, workflows are defined within the context of a flow. A flow is a Python function decorated with a @flow decorator. Every Prefect workflow must contain at least one flow function that serves as the entry point for execution of the flow. Flows can include calls to tasks as well as to child flows, which are called "subflows" in this context.

### Prefect flow

Here's an example of a Prefect flow that reads and preprocesses data from a file:
```
from prefect import flow, task

@task(retries=3, retry_delay_seconds=2, name="Read taxi data")
def read_data(filename: str) -> pd.DataFrame:
    # Read and preprocess the data
    ...

@flow
def main_flow(
    train_path: str = "~/mlops-zoomcamp/data/green_tripdata_2023-01.parquet",
    val_path: str = "~/mlops-zoomcamp/data/green_tripdata_2023-02.parquet",
) -> None:
    # Load the data
    df_train = read_data(train_path)
    df_val = read_data(val_path)
```

### Prefect task

A task is a function that represents a distinct piece of work executed within a flow. You can encapsulate your business logic into smaller task units, which gives you more granular observability, control over how specific tasks are run, and the ability to reuse tasks across flows and subflows. Tasks are created similarly to flows, using the @task decorator.

Here's an example of a Prefect task within a flow that adds features to the data:

```
@task
def add_features(
    df_train: pd.DataFrame, df_val: pd.DataFrame
) -> tuple(
    [
        scipy.sparse._csr.csr_matrix,
        scipy.sparse._csr.csr_matrix,
        np.ndarray,
        np.ndarray,
        sklearn.feature_extraction.DictVectorizer,
    ]
):
    # Add features to the data
    ...

@flow
def main_flow(
    train_path: str = "./data/green_tripdata_2023-01.parquet",
    val_path: str = "./data/green_tripdata_2023-02.parquet",
) -> None:
    # Load the data
    df_train = read_data(train_path)
    df_val = read_data(val_path)

    # Transform the data
    X_train, X_val, y_train, y_val, dv = add_features(df_train, df_val)
```

Not only can you call task functions within a flow, but you can also call other flow functions! Child flows are called subflows and allow you to efficiently manage, track, and version common multi-task logic.


[Previous](set_environment.md) | [Next](deploy.md)