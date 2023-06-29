# Batch Monitoring Pipeline for ML Models

The concept of batch monitoring pipelines for ML models is introduced. In a batch monitoring pipeline, data is collected over a period of time, and the model's performance is evaluated on this batch of data. This is different from real-time monitoring where the model's performance is evaluated continuously.


## Understanding Batch and Non-Batch Models

In the world of machine learning, we often work with two types of models: batch and non-batch. Understanding the differences between these two is crucial for effective monitoring.

- **Batch Models:** These models allow us to calculate many metrics in batch mode. For instance, drift detection methods require two distributions to compare, which we can obtain from a reference data set (like a validation set or a previous batch) and the most recent batch of data. Metrics like precision and recall can also be calculated on a batch of data.

- **Non-Batch Models:** These models, such as those operating as REST API services, present a different challenge. While we can calculate metrics like missing values or range violations in real time, for metrics like data drift or model performance, it's often better to generate a batch of data and then calculate those metrics.


## Utilizing Window Functions for Non-Batch Models

- For non-batch models, use window functions.
- Wait until a small batch of data has been collected, calculate the metrics on this batch, and then store the results.
- This approach allows for batch monitoring even for online machine learning services.


[Previous](intro.md) | [Next](scheme.md)