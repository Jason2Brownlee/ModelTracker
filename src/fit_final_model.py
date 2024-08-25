import sqlite3
import pickle
import argparse
from sklearn.datasets import load_iris
from custom_config import load_dataset

def fetch_serialized_model(db_path, experiment_id):
    """Fetches the serialized model (pipeline) from the database by experiment ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT serialized_pipeline
        FROM Experiments
        WHERE experiment_id = ?
        ''', (experiment_id,))
        result = cursor.fetchone()

    if result is None:
        raise ValueError(f"No experiment found with ID {experiment_id}")

    serialized_pipeline = result[0]
    return serialized_pipeline

def fit_final_model(db_path, experiment_id):
    """Fits the final model using all available data."""
    # Fetch the serialized model (pipeline) from the database
    serialized_pipeline = fetch_serialized_model(db_path, experiment_id)

    # Deserialize the pipeline
    pipeline = pickle.loads(serialized_pipeline)

    # Load the dataset
    X, y = load_dataset()

    # Fit the pipeline on all available data
    pipeline.fit(X, y)

    print(f"Final model for experiment ID {experiment_id} has been fitted on all available data.")

    return pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve and fit a final model on all available data.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")
    parser.add_argument("experiment_id", type=int, help="ID of the experiment to retrieve the model.")

    args = parser.parse_args()

    # Fit the final model
    final_model = fit_final_model(db_path=args.db_path, experiment_id=args.experiment_id)

    # The final model is now fitted on all data and can be used for further predictions or saved
    # You can save the final model if needed:
    # with open("final_model.pkl", "wb") as f:
    #     pickle.dump(final_model, f)
