import sqlite3
import pickle
import argparse
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import load_iris
from custom_config import load_dataset, default_resampling_method, default_evaluation_metric

def fetch_unrun_experiments(db_path):
    """Fetches all experiments that have not been run."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT experiment_id, experiment_name, serialized_pipeline, config
        FROM Experiments
        WHERE experiment_id NOT IN (SELECT DISTINCT experiment_id FROM Runs)
        ''')
        experiments = cursor.fetchall()
    return experiments


def evaluate_pipeline(pipeline, X, y, resample_method, eval_metric):
    """
    Evaluates the pipeline using the provided resampling method and evaluation metric.
    Returns the mean and standard deviation of the scores.
    """
    try:
        # Get the resampling method and its parameters
        resample_func, resample_params = resample_method(X, y)

        # Perform cross-validation and calculate the scores
        scores = resample_func(pipeline, X, y, scoring=eval_metric(), **resample_params)

        # Calculate mean and standard deviation of the scores
        mean_score = np.mean(scores)
        std_score = np.std(scores)

        return mean_score, std_score
    except Exception as e:
        print(f"Failed to evaluate pipeline: {e}")
        # Return NaN for both mean and standard deviation in case of an error
        return np.nan, np.nan

def execute_experiment(experiment_id, serialized_pipeline, X, y, db_path, resample_method, eval_metric):
    """Executes the experiment, saves the results in the Runs table."""
    # Deserialize the pipeline
    pipeline = pickle.loads(serialized_pipeline)

    # Start timing the execution
    start_time = datetime.now()

    # Evaluate the pipeline
    mean_score, std_score = evaluate_pipeline(pipeline, X, y, resample_method, eval_metric)

    # End timing
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Save the run results in the Runs table
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO Runs (experiment_id, run_date, score, duration, run_config, std_score)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (experiment_id, datetime.now().isoformat(), mean_score, duration, str(pipeline.get_params()), std_score))
        conn.commit()

def run_pending_experiments(db_path, resample_method=default_resampling_method, eval_metric=default_evaluation_metric):
    """Runs all experiments that have not been run yet."""
    # Load the dataset using the load_dataset function
    X, y = load_dataset()

    experiments = fetch_unrun_experiments(db_path)

    if not experiments:
        print("No pending experiments to run.")
        return

    for experiment in experiments:
        experiment_id, experiment_name, serialized_pipeline, config = experiment
        print(f"Running experiment: {experiment_name} (ID: {experiment_id})")
        execute_experiment(experiment_id, serialized_pipeline, X, y, db_path, resample_method, eval_metric)
        print(f"Experiment {experiment_name} completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run untested experiments from the database.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")

    args = parser.parse_args()

    # Run pending experiments with the provided database and dataset
    run_pending_experiments(db_path=args.db_path)

    print("All pending experiments have been executed.")


