# Baseline Data and Model

Before we can start monitoring our machine learning model, we need to establish a baseline. This involves gathering initial data and training a model that we can use as a reference point for future comparisons.

## Step 1: Import Libraries

First, we need to import all the necessary libraries for our project. This includes libraries for handling requests, datetime operations, data manipulation (Pandas), machine learning (Scikit-learn), model persistence (Joblib), progress bars (tqdm), and data drift and model performance monitoring (Evidently).

```
# Import necessary libraries
import requests
import datetime
import pandas as pd

# Import Evidently for data drift and model performance monitoring
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

# Import joblib for model persistence and tqdm for progress bars
from joblib import load, dump
from tqdm import tqdm

# Import sklearn for machine learning
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


## Step 2: Define Functions

Next, we define several functions that we will use throughout the project. These include:

- `download_files()`: This function downloads files from a specified URL and saves them to a local directory. It uses the `requests` library to send a GET request to the URL and download the file, and the `tqdm` library to display a progress bar.


```python
def download_files(files):
    # Print a message to indicate the start of the download process
    print("Download files:")

    # Loop over each file in the provided list
    for file, path in files:
        # Construct the URL for the file
        url=f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file}"

        # Send a GET request to the URL
        resp=requests.get(url, stream=True)

        # Construct the save path for the file
        save_path=f"{path}/{file}"

        # Open the save path in write-binary mode
        with open(save_path, "wb") as handle:
            # Loop over each chunk in the response content
            for data in tqdm(resp.iter_content(),
                            desc=f"{file}",
                            postfix=f"save to {save_path}",
                            total=int(resp.headers["Content-Length"])):
                # Write the chunk to the file
                handle.write(data)
```

- `preprocess_data()`: This function preprocesses the data by calculating the duration of each trip in minutes and filtering out trips with unrealistic durations and passenger counts. It uses the `pandas` library for data manipulation.

```python
def preprocess_data(df):
    # Calculate the duration of each trip in minutes
    # This is done by subtracting the pickup time from the dropoff time
    # The result is converted from seconds to minutes
    df["duration_min"] = (df.lpep_dropoff_datetime - df.lpep_pickup_datetime).dt.total_seconds() / 60

    # Filter out trips with unrealistic durations
    # We only keep trips with durations between 0 and 60 minutes
    df = df[(df.duration_min >= 0) & (df.duration_min <= 60)]

    # Filter out trips with unrealistic passenger counts
    # We only keep trips with passenger counts between 1 and 8
    df = df[(df.passenger_count > 0) & (df.passenger_count <= 8)]

    # Return the preprocessed data
    return df
```

- `train_and_evaluate()`: This function trains a Linear Regression model on the training data and evaluates it on the validation data. The script calculates the Mean Absolute Error (MAE) of the predictions on both the training and validation data.

```python
def train_and_evaluate(df, num_features, cat_features, target):
    # Split the data into training and validation sets
    train_data = df[:30000].copy()
    val_data = df[30000:].copy()

    # Initialize and train a Linear Regression model
    model = LinearRegression()
    model.fit(train_data[num_features + cat_features], train_data[target])

    # Make predictions on the training and validation sets
    train_preds = model.predict(train_data[num_features + cat_features])
    val_preds = model.predict(val_data[num_features + cat_features])

    # Add the predictions as a new column in the training and validation data
    train_data['prediction'] = train_preds
    val_data['prediction'] = val_preds

    # Print the mean absolute error of the model on the training and validation data
    print("Training Mean Absolute Error: ", mean_absolute_error(train_data.duration_min, train_data.prediction))
    print("Validation Mean Absolute Error: ", mean_absolute_error(val_data.duration_min, val_data.prediction))

    # Return the trained model and the training and validation data
    return model, train_data, val_data
```

- `save_model_and_data()`: This function saves the trained model and the validation data for future use. It uses the `joblib.dump` function to save the model and the `pandas.DataFrame.to_parquet` method to save the validation data.

```python
def save_model_and_data(model, df):
    with open('models/lin_reg.bin', 'wb') as f_out:
        dump(model, f_out)
    df.to_parquet('data/reference.parquet')
```

- `generate_report()`: This function generates an Evidently report that provides insights into the performance of the model. It specifies the target variable, prediction variable, and the numerical and categorical features. The report checks for column drift, dataset drift, and missing values in the dataset.

```python
def generate_report(train_data, val_data, num_features, cat_features):
    # Define the column mapping for the Evidently report
    # This includes the prediction column, numerical features, and categorical features
    column_mapping = ColumnMapping(
        target=None,
        prediction='prediction',
        numerical_features=num_features,
        categorical_features=cat_features
    )

    # Initialize the Evidently report with the desired metrics
    # In this case, we're using the ColumnDriftMetric for the 'prediction' column,
    # the DatasetDriftMetric to measure drift across the entire dataset,
    # and the DatasetMissingValuesMetric to measure the proportion of missing values
    report = Report(metrics=[
        ColumnDriftMetric(column_name='prediction'),
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ])

    # Run the report on the training and validation data
    # The training data is used as the reference data, and the validation data is the current data
    report.run(reference_data=train_data, current_data=val_data, column_mapping=column_mapping)

    # Return the generated report
    return report
```

## Step 3: Download Data

We'll download the Green Taxi Trip Data from January and February 2022 using the `download_files()` function. This data is publicly available and can be used for our machine learning project.

```
files = [('green_tripdata_2022-02.parquet', './data'), ('green_tripdata_2022-01.parquet', './data')]
download_files(files)
```

## Step 4: Load and Preprocess Data

After downloading the data, we'll load it into a pandas DataFrame and preprocess it
```
jan_data = pd.read_parquet('data/green_tripdata_2022-01.parquet')
jan_data = preprocess_data(jan_data)
```

## Step 5: Define Features and Target

We'll define the features we want to use for our model and the target variable. The features are the variables that our model will use to make predictions, while the target is the variable that we want to predict. In this case, we're trying to predict the duration of a taxi trip (in minutes) based on the passenger count, trip distance, fare amount, total amount, and pickup and dropoff locations.
```
target = "duration_min"
num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
cat_features = ["PULocationID", "DOLocationID"]
```

## Step 6: Train and Evaluate Model

We'll train a linear regression model on the training data and evaluate it on the validation data using the `train_and_evaluate()` function. This step involves fitting the model to the training data and then using it to make predictions on the validation data. We then calculate the mean absolute error of the predictions to evaluate the model's performance.

```
model, train_data, val_data = train_and_evaluate(jan_data, num_features, cat_features, target)
```

## Step 7: Save Model and Reference Data

Finally, we'll save the trained model and reference data for future use using the `save_model_and_data()` function. This step is important for model deployment and monitoring, as we'll need to load the model and reference data in the future.
```
save_model_and_data(model, val_data)
```

Step 8: Generate Evidently Report

We'll generate an Evidently report to monitor the performance of our model using the `generate_report()` function. This report provides insights into the model's performance and can help us identify any issues or areas for improvement.
```
report = generate_report(train_data, val_data, num_features, cat_features)
```

![report](https://github.com/dimzachar/capstone_mlzoomcamp/blob/master/Extra/kaggle.png)


## Step 9: Extract Key Metrics and Display Report

We'll extract key metrics such as the drift score, the number of drifted columns, and the share of missing values. from the report and print them. These metrics can give us a quantitative measure of the model's performance and any data drift. We'll then display the Evidently report, which provides a visual representation of these metrics.

```
result = report.as_dict()
print("Drift score of the prediction column: ", result['metrics'][0]['result']['drift_score'])
print("Number of drifted columns: ", result['metrics'][1]['result']['number_of_drifted_columns'])
print("Share of missing values: ", result['metrics'][2]['result']['current']['share_of_missing_values'])
report.show(mode='inline')
```

- **Drift score of the prediction column:**  This is the drift score for the prediction column, which measures how much the predictions have changed compared to the reference data.
- **Number of drifted columns:** This is the number of columns in the data that have drifted, or changed significantly, compared to the reference data.
- **Share of missing values:** This is the proportion of missing values in the current data.


That's it! We now have your source datasets for January and February, a reference dataset for calculating metrics, a model for simulating the production usage of the duration prediction service. We also calculated metrics for monitoring.
Next, we will see how to create dummy metrics, set up and access a database for a Grafana dashboard. Stay tuned!


[Previous](docker_compose.md) | [Next](dummy_monitoring.md)