# Environment Setup with Docker Compose

## Step 1: Create a Working Directory

First, we need to create a working directory for our project. Open your terminal and run the following command:

```
mkdir taxi_monitoring
```

## Step 2: Set Up a Conda Environment

Next, we'll create a Conda virtual environment with Python 3.11. In your terminal, run:

```
conda create -n py11 python=3.11
conda activate py11
```


## Step 3: Create a Requirements.txt File

We'll create a `requirements.txt` file to list all the necessary Python libraries for our project. Here's an example of what this file might look like:

```
prefect
tqdm
requests
joblib
psycopg2-binary
pandas
numpy
scikit-learn
jupyter
```

## Step 4: Install Python Packages

Now, we'll install all the Python packages listed in the `requirements.txt` file. In your terminal, navigate to the directory containing `requirements.txt` and run:

```bash
pip install -r requirements.txt
```

[Previous](scheme.md) | [Next](docker_compose.md)