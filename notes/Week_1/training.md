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

This chapter covers the process of building an ML model for predicting ride duration, which involves loading and filtering data, parsing datetime, applying a lambda function, visualizing distribution, data analysis and variable selection, adding features with one-hot encoding, linear regression model evaluation using RMSE, model training and evaluation with linear regression and Lasso, exploring validation and Lasso model for linear regression, combining features to reduce error in prediction, and saving the linear regression model with a dictionary and vectorizer. The key takeaway from this chapter is understanding the data science approach to model training and how to build a machine learning model for predicting ride duration.


<div align="center">
    <img src="https://showme.redstarplugin.com/s/LnQTZzp3" />
</div>

[Previous](update_ssh_config.md) | [Next](best-practices.md)