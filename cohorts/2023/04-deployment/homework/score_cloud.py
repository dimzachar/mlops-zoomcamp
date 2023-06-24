import pickle
import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, required=True)
parser.add_argument('--month', type=int, required=True)
parser.add_argument('--taxi_type', type=str, required=True)  # Add this line
args = parser.parse_args()

# Use the year, month, and taxi type provided by the user
year = args.year
month = args.month
taxi_type = args.taxi_type

# Define the output directory
output_dir = 'output'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Define the input file URL and output file path
input_file = f's3://nyc-tlc/trip data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f's3://nyc-taxi-za/taxi_type={taxi_type}/year={year:04d}/month={month:02d}/predictions.parquet'
# Load the model and vectorizer
try:
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
except FileNotFoundError:
    print("Error: The model file 'model.bin' was not found.")
    exit(1)
    

categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

df = read_data(input_file)


dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)


print(f"Predicted mean duration {y_pred.mean():.2f}")


# Prepare a DataFrame with the ride_id and predicted_duration

df_result = pd.DataFrame()
# Create 'ride_id' column
df_result['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
df_result['predicted_duration'] = y_pred

# Save the DataFrame to a parquet file
df_result.to_parquet(
    output_file,
    engine='pyarrow',
    compression=None,
    index=False
)



