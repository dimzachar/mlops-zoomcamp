# Debugging with test suites and reports

In this tutorial, we will explore how to debug and monitor machine learning models using the Evidently library. Debugging involves identifying, isolating, and fixing issues that may affect the performance of a machine learning model. Monitoring, on the other hand, is the continuous observation of the model's performance over time to detect any significant changes or anomalies.

One of the key challenges in monitoring machine learning models is detecting "drift". Drift refers to the change in statistical properties of the model's input data over time. This change can lead to a decline in the model's predictive performance, as the model's assumptions about the data no longer hold. Detecting drift is crucial as it allows us to proactively update or retrain the model to maintain its performance.

Evidently provides powerful tools for both debugging and monitoring. It offers Test Suites and Reports that help in understanding the model's behavior and performance.

Test Suites in Evidently allow us to run a series of tests on the data to check for various conditions, such as data drift. If any of the tests fail, it indicates a potential issue that needs to be debugged.

Reports in Evidently provide a comprehensive analysis of the data and the model. They calculate various metrics and provide visualizations that help in understanding the state of the data and the model. For instance, a [Data Drift](https://docs.evidentlyai.com/presets/data-drift) report can show how the features' distributions have changed over time, indicating drift.

By leveraging these tools, we can effectively debug and monitor our machine learning models, ensuring their robustness and reliability in production environments.

## Step 1: Import Libraries

We start by importing the necessary libraries. These include pandas for data manipulation, joblib for loading the trained model, and various components from the Evidently library for drift detection and reporting. We also import the LinearRegression model and metrics from sklearn for model evaluation.

```python
import datetime
import pandas as pd
from joblib import dump, load
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently.test_suite import TestSuite
from evidently.test_preset import DataDriftTestPreset
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
```

## Step 2: Load Data and Model

Next, we load the data that we want to analyze and the model we want to monitor. In this case, we are interested in the data from February 2nd, which showed a high data drift value for our prediction function. We also define the target variable and the features that our model uses.

![debugging](https://github.com/dimzachar/capstone_mlzoomcamp/blob/master/Extra/kaggle.png)

The `ref_data` is the reference data that the model was trained on, and `current_data` is the new data that we want to analyze for drift. The `problematic_data` is a subset of the `current_data` that corresponds to the time when the drift occurred. This subset is what we will use for our analysis.

```python
ref_data = pd.read_parquet('data/reference.parquet')
current_data = pd.read_parquet('data/green_tripdata_2022-02.parquet')

with open('models/lin_reg.bin', 'rb') as f_in:
    model = load(f_in)

target = "duration_min"
num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
cat_features = ["PULocationID", "DOLocationID"]

problematic_data = current_data.loc[(current_data.lpep_pickup_datetime >= datetime.datetime(2022,2,2,0,0)) & 
                               (current_data.lpep_pickup_datetime < datetime.datetime(2022,2,3,0,0))]
```

## Step 3: Generate Test Suite and Report

We then generate a test suite using Evidently to see which tests related to data drift failed. This involves creating a test suite object, running the test suite, and visualizing the test results. 

The `ColumnMapping` object is used to specify the structure of the data, including the prediction column, numerical features, and categorical features. The target is set to None because we are not interested in the target variable for this analysis.

We then add the model's predictions to the `problematic_data` DataFrame. This is done by applying the model's `predict` method to the features in the `problematic_data`.

The `TestSuite` object is created with a list of tests to run, in this case, the `DataDriftTestPreset`. The test suite is then run on the reference data and the problematic data, and the results are displayed inline in the notebook.

We also generate a report using Evidently to support our analysis and debug the data. This involves creating a report object, running the report, and visualizing the report.

The `Report` object is created with a list of metrics to calculate, in this case, the `DataDriftPreset`. The report is then run on the reference data and the problematic data, and the results are displayed inline in the notebook.

```python
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

problematic_data['prediction'] = model.predict(problematic_data[num_features + cat_features].fillna(0))

test_suite = TestSuite(tests = [DataDriftTestPreset()])
test_suite.run(reference_data=ref_data, current_data=problematic_data, column_mapping=column_mapping)
test_suite.show(mode='inline')

report = Report(metrics = [DataDriftPreset()])
report.run(reference_data=ref_data, current_data=problematic_data, column_mapping=column_mapping)
report.show(mode='inline')
```

By following these steps, we can effectively debug and monitor our machine learning models, allowing us to identify and understand any changes in the model's performance over time. This information can be crucial for maintaining the performance of deployed models, as it allows us to take action (such as retraining the model) when drift is detected.

[Previous](save_dashboard.md)