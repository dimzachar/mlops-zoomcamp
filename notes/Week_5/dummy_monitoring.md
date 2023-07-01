# Dummy monitoring

In this tutorial, we will be creating a database and tables for dummy metrics calculation. We will start by preparing the database and creating tables with dummy data. Next, we will insert timestamp values into the database table. Finally, we will set up and access a PostgreSQL database for Grafana dashboard. 

Here is a breakdown of `dummy_metrics_calculation.py` :

## Step 1: Import Libraries

First, we need to import the necessary libraries. These include:

- `datetime` and `pytz` for handling date and time.
- `random` and `uuid` for generating random values.
- `logging` for logging information in the terminal.
- `psycopg2` for accessing the PostgreSQL database.
- `pandas` for handling data.

```python
import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
```

## Step 2: Define Constants and SQL Statement

Next, we define a constant for the send timeout and an SQL statement to create the `dummy_metrics` table.

```
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
    timestamp timestamp,
    value1 integer,
    value2 varchar,
    value3 float
)
"""
```

## Step 3: Define Functions

Next, we define two main functions:

- `prep_db()` : This function prepares the database by checking if the test database exists. If it doesn't, it creates the database and then creates a table for dummy metrics.

```
def prep_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
        if len(res.fetchall()) == 0:
            conn.execute("create database test;")
        with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
            conn.execute(create_table_statement)
```

- `calculate_dummy_metrics_postgresql()` : This function calculates dummy metrics and loads them into the table. It generates random values for three variables and inserts them into the table along with the current timestamp.

```
def calculate_dummy_metrics_postgresql(curr):
    value1 = rand.randint(0, 1000)
    value2 = str(uuid.uuid4())
    value3 = rand.random()

    curr.execute(
        "insert into dummy_metrics(timestamp, value1, value2, value3) values (%s, %s, %s, %s)",
        (datetime.datetime.now(pytz.timezone('Europe/London')), value1, value2, value3)
    )
```

## Step 4: Main Function

In the main function, we prepare the database and then run a loop to calculate and insert dummy metrics into the table. We also calculate the time delay to simulate real production usage.

```
def main():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 100):
			with conn.cursor() as curr:
				calculate_dummy_metrics_postgresql(curr)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")

if __name__ == '__main__':
	main()
```

## Step 5: Test the Script

Now, let's test our script

```
python dummy_metrics_calculation.py
```

## Step 6: Check the Database

Go to the browser and take a look at our database. We have a table `dummy_metrics` which is good. This is the schema of the table and we can select some data. We see that we have quite a lot already here is a timestamp, value 1, value 2, and value 3.

![dummy_metrics](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/dummy_metrics.png)

## Step 7: Access Data from Grafana

Now, let's go to Grafana and see whether we are able to access those data from Grafana. If we configured our Grafana and PostgreSQL correctly, we should be able to create a new dashboard. Here, we can see the example of a panel which is auto-generated, but we need to choose our data source which is PostgreSQL. We can select value for example, let's select value one and we can see the preview of our plot. We can change the last six hours to last five minutes so we can observe more of our data. Maybe add some description or change the panel name. Let's just create that, it's our dummy metric. Here, we can see our panel. It looks pretty nicely in Grafana. We can customize our own dashboard. We can add more panels here. For example, let's now select value 3 and call it Dummy Value 3. Maybe we want to change the color here. Violet for example. And here is our practical straightforward dashboard.

So basically now we are sure that we correctly created all the configuration files so we can actually access our database, load data here, and build some dashboard from Grafana.

![dummy_dashboard](https://github.com/dimzachar/mlops-zoomcamp/blob/master/notes/Week_5/Images/dummy_dashboard.png)

[Previous](baseline.md) | [Next](data_quality.md)