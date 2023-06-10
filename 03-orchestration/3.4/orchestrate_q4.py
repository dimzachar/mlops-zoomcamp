import pathlib
import pickle
import pandas as pd
import numpy as np
import scipy
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import mlflow
import xgboost as xgb
from prefect import flow, task

@task(retries=3, retry_delay_seconds=2, name="Read taxi data")
def read_data(filename: str) -> pd.DataFrame:
    """
    Read data from a file into a pandas DataFrame and preprocess it.
    
    Parameters:
    filename (str): The path to the file to read.

    Returns:
    pd.DataFrame: The preprocessed data.
    """
    # Read the data from the file
    df = pd.read_parquet(filename)

    # Convert the datetime columns to datetime objects
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)

    # Calculate the duration of the trip in minutes
    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    # Filter out trips with unrealistic durations
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    # Convert the location ID columns to strings
    categorical = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    return df

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
    """
    Add features to the data and convert it to a format suitable for training a model.
    
    Parameters:
    df_train (pd.DataFrame): The training data.
    df_val (pd.DataFrame): The validation data.

    Returns:
    tuple: The transformed training and validation data, the target values, and the DictVectorizer object used for the transformation.
    """
    # Add a new feature that combines the pickup and dropoff location IDs
    df_train["PU_DO"] = df_train["PULocationID"] + "_" + df_train["DOLocationID"]
    df_val["PU_DO"] = df_val["PULocationID"] + "_" + df_val["DOLocationID"]

    # Define the categorical and numerical features
    categorical = ["PU_DO"]  #'PULocationID', 'DOLocationID']
    numerical = ["trip_distance"]

    # Initialize a DictVectorizer
    dv = DictVectorizer()

    # Convert the training data to a format suitable for the DictVectorizer and transform it
    train_dicts = df_train[categorical + numerical].to_dict(orient="records")
    X_train = dv.fit_transform(train_dicts)

    # Convert the validation data to a format suitable for the DictVectorizer and transform it
    val_dicts = df_val[categorical + numerical].to_dict(orient="records")
    X_val = dv.transform(val_dicts)

    # Extract the target values
    y_train = df_train["duration"].values
    y_val = df_val["duration"].values

    return X_train, X_val, y_train, y_val, dv

@task(log_prints=True)
def train_best_model(
    X_train: scipy.sparse._csr.csr_matrix,
    X_val: scipy.sparse._csr.csr_matrix,
    y_train: np.ndarray,
    y_val: np.ndarray,
    dv: sklearn.feature_extraction.DictVectorizer,
) -> None:
    """
    Train an XGBoost model with the best hyperparameters, evaluate it, and save the model and the DictVectorizer object.
    
    Parameters:
    X_train (scipy.sparse._csr.csr_matrix): The training data.
    X_val (scipy.sparse._csr.csr_matrix): The validation data.
    y_train (np.ndarray): The target values for the training data.
    y_val (np.ndarray): The target values for the validation data.
    dv (sklearn.feature_extraction.DictVectorizer): The DictVectorizer object used to transform the data.

    Returns:
    None
    """
    # Start an MLflow run
    with mlflow.start_run():
        # Convert the data to a format suitable for XGBoost
        train = xgb.DMatrix(X_train, label=y_train)
        valid = xgb.DMatrix(X_val, label=y_val)

        # Define the best hyperparameters
        best_params = {
            "learning_rate": 0.09585355369315604,
            "max_depth": 30,
            "min_child_weight": 1.060597050922164,
            "objective": "reg:linear",
            "reg_alpha": 0.018060244040060163,
            "reg_lambda": 0.011658731377413597,
            "seed": 42,
        }

        # Log the hyperparameters to MLflow
        mlflow.log_params(best_params)

        # Train the model
        booster = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=100,
            evals=[(valid, "validation")],
            early_stopping_rounds=20,
        )

        # Make predictions on the validation data
        y_pred = booster.predict(valid)

        # Calculate the RMSE
        rmse = mean_squared_error(y_val, y_pred, squared=False)

        # Log the RMSE to MLflow
        mlflow.log_metric("rmse", rmse)

        # Create a directory for the models if it doesn't exist
        pathlib.Path("models").mkdir(exist_ok=True)

        # Save the DictVectorizer object
        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)

        # Log the DictVectorizer object to MLflow
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")

        # Log the model to MLflow
        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")
        
        markdown__rmse_report = f"""# RMSE Report

        ## Summary

        Duration Prediction 

        ## RMSE XGBoost Model

        | Region    | RMSE |
        |:----------|-------:|
        | {date.today()} | {rmse:.2f} |
        """

        create_markdown_artifact(
            key="duration-model-report", markdown=markdown__rmse_report
        )

    return None

    return None

@flow
def main_flow_q4(
    train_path: str = "~/mlops-zoomcamp/data/green_tripdata_2023-02.parquet",
    val_path: str = "~/mlops-zoomcamp/data/green_tripdata_2023-03.parquet",
) -> None:
    """
    The main training pipeline.
    
    Parameters:
    train_path (str): The path to the training data file.
    val_path (str): The path to the validation data file.

    Returns:
    None
    """
    # Set the MLflow tracking URI and experiment name
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("nyc-taxi-experiment")

    # Load the data
    df_train = read_data(train_path)
    df_val = read_data(val_path)

    # Transform the data
    X_train, X_val, y_train, y_val, dv = add_features(df_train, df_val)

    # Train the model
    train_best_model(X_train, X_val, y_train, y_val, dv)


if __name__ == "__main__":
    """
    If the script is run (as opposed to being imported), execute the main pipeline.
    """
    main_flow_q4()
