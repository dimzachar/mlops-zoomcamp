# Building ML Model for Predicting Ride Duration

## Reading Parquet Files Using Pandas

Parquet is a columnar storage file format that is optimized for use with big data processing frameworks. We learn how to read Parquet file format using Pandas in Jupyter Notebook.

```
pip install pyarrow
```

```
# Read the Parquet file
df = pd.read_parquet('example.parquet')

# Display the DataFrame
print(df)
```

## Training a ride duration prediction model

* Understand the process of predicting ride duration using a machine learning model.
* Load and filter data using scikit-learn.
* Discover how to build a regression model with trip distance as a feature.
* Calculate duration using pandas datetime functions and convert it to minutes for the machine learning model.
* Analyze the duration column and visualize its distribution.
* Add features to a model and implement one hot encoding using dictionary vectorizer.
* Apply a linear regression model to training data and evaluate its performance.

[Previous](update_ssh_config.md) | [Next](best-practices.md)