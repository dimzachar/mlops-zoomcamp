# Data Quality Monitoring

In this tutorial, we delve into a crucial aspect of Machine Learning Operations (MLOps) - monitoring the performance of deployed machine learning models over time. The primary objective is to identify and log any changes in the model's performance, a process known as "drift detection". Drift can occur when the statistical properties of the target variable, which the model aims to predict, alter unexpectedly over time, potentially leading to a decline in the model's performance.

To orchestrate the tasks involved in calculating and storing drift metrics, we employ the Prefect library. The Evidently library is utilized to compute three types of metrics:

- **Column Drift:** Measures if the statistical properties of individual features (columns) have changed.
- **Dataset Drift:** Measures if the statistical properties of the entire dataset have changed.
- **Missing Values:** Measures the proportion of missing values in the dataset.

These metrics, computed for each day's data, are stored in a PostgreSQL database for subsequent analysis. Designed to operate as a batch job, the script processes a large volume of data at once, instead of handling each data point individually in real-time.

Included in the script is a function to prepare the database, creating the necessary table if it doesn't already exist. The metrics are then inserted into this table for each day's data. With periodic execution (e.g., daily), the script enables continuous monitoring of the model's performance, providing early warning signs if performance is deteriorating due to drift. This information can trigger model retraining or other interventions to maintain performance.

Finally, we demonstrate how to construct a dashboard with panels and metrics in Grafana, offering a visual representation of the model's performance and any detected drift.

## Step 1: Import Libraries

We start by importing the necessary libraries

```python
import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
```


## Step 2: Define Global Variables

In this step, we define several global variables that will be used throughout the script. These variables are used to set up the environment for our model monitoring task.
We define the timeout for sending metrics to the database, create a random number generator for any random operations, and specify the SQL statement to create a table in the database for storing our metrics.
We also load our reference data and trained model from their respective files, and specify the raw data that will be used for model prediction and evaluation.
We set the beginning of the time period for which the metrics are calculated, and specify the numerical and categorical features used in the model.
Finally, we set up the column mapping for the Evidently report and create an Evidently report object, which will be used to calculate and visualize the metrics.

Here's the code that defines these global variables:

```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
    timestamp timestamp,
    prediction_drift float,
    num_drifted_columns integer,
    share_missing_values float
)
"""

reference_data = pd.read_parquet('data/reference.parquet')
with open('models/lin_reg.bin', 'rb') as f_in:
    model = joblib.load(f_in)

raw_data = pd.read_parquet('data/green_tripdata_2022-02.parquet')

begin = datetime.datetime(2022, 2, 1, 0, 0)
num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

report = Report(metrics = [
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])
```

## Step 3: Define Tasks

In this step, we define several tasks that will be used in our Prefect pipeline. These include:

1. `prep_db()`: This task prepares the database by creating a new database and a table for storing the metrics.


```python
@task
def prep_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
        with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
            conn.execute(create_table_statement)
```


2. `calculate_metrics_postgresql()`: This task calculates the metrics for a given time period and inserts them into the database. It uses the Evidently report to calculate the metrics.

```python
@task
def calculate_metrics_postgresql(curr, i):
    current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
        (raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

    current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

    report.run(reference_data = reference_data, current_data = current_data,
        column_mapping=column_mapping)

    result = report.as_dict()

    prediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

    curr.execute(
        "insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
        (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
    )
```

3. `batch_monitoring_backfill()`: This task orchestrates the entire process. It calls the `prep_db()` task to prepare the database, then loops over each day in the time period, calls the `calculate_metrics_postgresql()` task to calculate the metrics for that day, and inserts them into the database. It also ensures that the metrics are sent to the database at a rate that does not exceed the `SEND_TIMEOUT`.


```python
@flow
def batch_monitoring_backfill():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

            new_send = datetime.datetime.now()
            seconds_elapsed = (new_send - last_send).total_seconds()
            if seconds_elapsed < SEND_TIMEOUT:
                time.sleep(SEND_TIMEOUT - seconds_elapsed)
            while last_send < new_send:
                last_send = last_send + datetime.timedelta(seconds=10)
            logging.info("data sent")

if __name__ == '__main__':
    batch_monitoring_backfill()
```

## Step 4: Start Prefect server

Start the Prefect server
```python
prefect server start
```

## Step 5: Run the Script

We run the script:
```python
python evidently_metrics_calculation.py
```

We can access the Prefect UI through `http://127.0.0.1:4200` and navigate `localhost:8080` to observe that the metrics table was created.

![prefect](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/prefect.png)

![table_metrics](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/table_metrics.png)

## Step 6: Grafana dashboard

Finally, we build a dashboard with panels and metrics in Grafana. 

![data_dashboard](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/data_dashboard.png)
![data_dashboard1](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/data_dashboard1.png)


Next, we will discuss how to save the dashboard and ensure it can be loaded every time the Docker container is rerun.


[Previous](dummy_monitoring.md) | [Next](save_dashboard.md)