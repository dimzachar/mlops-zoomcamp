# Introduction to MLOps Monitoring

![logo](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/logo.png)

Monitoring is a crucial part of MLOps. It involves tracking the performance of machine learning models in production, system metrics, data quality, and more. 
Over time, the quality of models can degrade, and monitoring can help detect this. Service health monitoring is essential to ensure the service is functioning correctly. 
This tutorial will guide you through the process of setting up a comprehensive monitoring system using Evidently and Grafana.

![service](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/service.png)

Evidently is an open-source Python library designed for data scientists and machine learning engineers. It's used to evaluate, test, and monitor the performance of machine learning models from the validation phase to production. Evidently works with tabular and text data and integrates into various ML stacks as a monitoring or evaluation component. It allows you to analyze the behavior of your models and detect potential issues early.


## Metrics for Model Performance and Data Quality

Monitoring the performance of the model and the quality of the data is necessary. The specific metrics used for this will depend on the problem statement. For example, if you work with ranking algorithms such as in search engine optimization or content recommender systems, you need to use ranking metrics.

## Reuse of Existing Monitoring Architecture for ML

Existing monitoring architecture can be reused for ML models. This means that the infrastructure and systems already in place for monitoring traditional software applications can also be used to monitor ML models. This can save time and resources as you don't need to build a new monitoring system from scratch.


[Next](batch.md)