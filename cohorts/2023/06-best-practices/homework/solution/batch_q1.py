import pickle
import pandas as pd
import sys

def read_data(filename, categorical):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def main(year, month):
    # Define the input file URL and output file path
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'taxi_type=yellow_year={year:04d}_month={month:02d}.parquet'


    # Load the model and vectorizer
    try:
        with open('model.bin', 'rb') as f_in:
            dv, model = pickle.load(f_in)
    except FileNotFoundError:
        print("Error: The model file 'model.bin' was not found.")
        exit(1)

    categorical = ['PULocationID', 'DOLocationID']

    print("Reading data...")
    df = read_data(input_file, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    
    
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)

    print("Making predictions...")
    y_pred = model.predict(X_val)

    print(f"Predicted mean duration: {y_pred.mean():.2f}")

    # Prepare a DataFrame with the ride_id and predicted_duration
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred

    print("Saving results...")
    df_result.to_parquet(output_file, engine='pyarrow', index=False)

    print("Process completed successfully.")

if __name__ == '__main__':
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
