import os
import pickle
import click
from functools import partial

import wandb

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

    
def load_pickle(filename: str):
    """Load a pickle file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found.")
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)
    
    
def run_train(data_artifact: str):
    """Run a training job with hyperparameters from WandB."""
    # Initialize a wandb run
    wandb.init()
    # Access configuration parameters through wandb.config
    config = wandb.config

    # Fetch the preprocessed dataset from artifacts
    artifact = wandb.use_artifact(data_artifact, type="preprocessed_dataset")
    data_path = artifact.download()

    # Load training and validation data
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    # Define the RandomForestRegressor model, train the model, and perform prediction
    # Parameters are fetched from `config`
    rf = RandomForestRegressor(max_depth=config.max_depth,
                               n_estimators=config.n_estimators,
                               min_samples_split=config.min_samples_split,
                               min_samples_leaf=config.min_samples_leaf,
                               random_state=0)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_val)

    # Calculate MSE and log it to wandb
    mse = mean_squared_error(y_val, y_pred, squared=False)
    wandb.log({"MSE": mse})

    # Save the trained model as a pickle file
    with open("regressor.pkl", "wb") as f:
        pickle.dump(rf, f)

    # Create an artifact for the trained model and log it to wandb
    artifact = wandb.Artifact(f"{wandb.run.id}-model", type="model")
    artifact.add_file("regressor.pkl")
    wandb.log_artifact(artifact)


# Configuration for the hyperparameter sweep
SWEEP_CONFIG = {
    "method": "bayes",
    "metric": {"name": "MSE", "goal": "minimize"},
    "parameters": {
        "max_depth": {
            "distribution": "int_uniform",
            "min": 1,
            "max": 20,
        },
        "n_estimators": {
            "distribution": "int_uniform",
            "min": 10,
            "max": 50,
        },
        "min_samples_split": {
            "distribution": "int_uniform",
            "min": 2,
            "max": 10,
        },
        "min_samples_leaf": {
            "distribution": "int_uniform",
            "min": 1,
            "max": 4,
        },
    },
}

@click.command()
@click.option("--wandb_project", help="Name of Weights & Biases project")
@click.option("--wandb_entity", help="Name of Weights & Biases entity")
@click.option("--data_artifact", help="Address of the Weights & Biases artifact holding the preprocessed data")
@click.option("--count", default=5, help="Number of iterations in the sweep")
def run_sweep(wandb_project: str, wandb_entity: str, data_artifact: str, count: int):
    """Run a hyperparameter sweep using wandb."""
    # Initialize the sweep
    sweep_id = wandb.sweep(SWEEP_CONFIG, project=wandb_project, entity=wandb_entity)
    # Run the sweep agent
    wandb.agent(sweep_id, partial(run_train, data_artifact=data_artifact), count=count)


if __name__ == "__main__":
    run_sweep()