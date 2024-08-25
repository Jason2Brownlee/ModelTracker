
import sqlite3
import pickle
import hashlib
from sklearn.base import BaseEstimator
from typing import Union

class ExperimentManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _hash_pipeline(self, pipeline: Union[BaseEstimator, 'Pipeline']) -> str:
        serialized_pipeline = pickle.dumps(pipeline)
        return hashlib.sha256(serialized_pipeline).hexdigest()

    def add_experiment(self, experiment_name: str, model: Union[BaseEstimator, 'Pipeline'], config: dict = None, description: str = None):
        # Serialize the model or pipeline
        serialized_pipeline = pickle.dumps(model)

        # Compute the hash of the pipeline
        pipeline_hash = self._hash_pipeline(model)

        # Convert config dictionary to a string (if provided)
        config_str = str(config) if config else None

        # Connect to the database and insert the new experiment
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute('''
                INSERT INTO Experiments (experiment_name, serialized_pipeline, config, pipeline_hash, description)
                VALUES (?, ?, ?, ?, ?)
                ''', (experiment_name, serialized_pipeline, config_str, pipeline_hash, description))
                conn.commit()
                print(f"Experiment '{experiment_name}' added successfully.")
            except sqlite3.IntegrityError:
                print(f"Experiment '{experiment_name}' already exists in the database (pipeline hash collision). Skipping insert.")

    def list_experiments(self):
        # List all experiments stored in the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT experiment_id, experiment_name, status FROM Experiments')
            experiments = cursor.fetchall()

        return experiments
