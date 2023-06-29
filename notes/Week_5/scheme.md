# Building a Monitoring Scheme

Now, let's build a monitoring scheme! This scheme can be applied to both batch and non-batch machine learning models. Here's how it works:

1. **Start with a Software Service:** This could be either a batch or non-batch service.

2. **Create a Pipeline:** This pipeline should read prediction logs in batches, calculate data and machine learning related metrics, and store them in a database.

3. **Build a Dashboard:** Use the database as a source for a dashboarding tool to visualize your metrics.

## Implementing the Monitoring Scheme

Let's put our scheme into action! Here's a step-by-step guide:

- **Use a Prediction Service:** For this tutorial, we'll use a service that predicts the duration of taxi trips. This service could be implemented as a REST API service or a batch prediction pipeline.

- **Simulate Production Usage:** Generate logs by simulating the production usage of this service.

- **Implement Monitoring Jobs:** Use Prefect to implement your monitoring jobs and the Evidently library to calculate metrics.

- **Load Metrics into a Database:** Load the calculated metrics into a PostgreSQL database.

- **Build a Dashboard:** Use Grafana to build a dashboard with the data from your PostgreSQL database.


[Previous](batch.md) | [Next](setup_env.md)
