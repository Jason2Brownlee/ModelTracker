import sqlite3
import os
import sys

def create_database(db_path):
    # Check if the database file already exists
    if os.path.exists(db_path):
        print(f"Error: Database '{db_path}' already exists.")
        sys.exit(1)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the Experiments table with the updated schema
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Experiments (
        experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_name TEXT NOT NULL,
        serialized_pipeline BLOB NOT NULL,
        config TEXT,
        pipeline_hash TEXT UNIQUE NOT NULL,
        creation_date TEXT DEFAULT CURRENT_TIMESTAMP,
        description TEXT,
        status TEXT DEFAULT 'created'
    )
    ''')

    # Create the Runs table with mean and standard deviation columns
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        experiment_id INTEGER,
        run_date TEXT DEFAULT CURRENT_TIMESTAMP,
        score REAL,
        std_score REAL,
        duration REAL,
        run_config TEXT,
        FOREIGN KEY (experiment_id) REFERENCES Experiments (experiment_id)
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_database.py <db_path>")
        sys.exit(1)

    db_path = sys.argv[1]
    create_database(db_path)
    print(f"Database created successfully at {db_path}.")
