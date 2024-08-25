import sqlite3
import argparse

def fetch_top_experiments(db_path, top_n=5):
    """Fetches the top n experiments based on the mean score."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT e.experiment_id, e.experiment_name, r.score, r.std_score, e.config
        FROM Runs r
        JOIN Experiments e ON r.experiment_id = e.experiment_id
        ORDER BY r.score DESC
        LIMIT ?
        ''', (top_n,))
        top_experiments = cursor.fetchall()
    return top_experiments

def report_top_experiments(top_experiments):
    """Prints the top experiments to the command line."""
    if not top_experiments:
        print("No experiments found.")
        return

    print(f"{'Rank':<5} {'Experiment ID':<15} {'Experiment Name':<30} {'Mean Score':<12} {'Std Dev':<10}")
    print("="*80)

    for rank, experiment in enumerate(top_experiments, start=1):
        experiment_id, experiment_name, score, std_score, config = experiment
        print(f"{rank:<5} {experiment_id:<15} {experiment_name:<30} {score:<12.4f} {std_score:<10.4f}")

    print("\nUse the Experiment ID to retrieve the configuration or serialized model.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report the top n experimental run results from the database.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")
    parser.add_argument("--top_n", type=int, default=5, help="Number of top experiments to report.")

    args = parser.parse_args()

    # Fetch the top n experiments
    top_experiments = fetch_top_experiments(db_path=args.db_path, top_n=args.top_n)

    # Report the top experiments
    report_top_experiments(top_experiments)
