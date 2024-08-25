import sqlite3
import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def fetch_top_experiments(db_path, top_n=10):
    """Fetches the top n experiments based on the mean score."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT e.experiment_id, e.experiment_name, r.score, r.std_score, r.duration
        FROM Runs r
        JOIN Experiments e ON r.experiment_id = e.experiment_id
        ORDER BY r.score DESC
        LIMIT ?
        ''', (top_n,))
        top_experiments = cursor.fetchall()
    return top_experiments

def fetch_all_scores(db_path):
    """Fetches all scores from the Runs table."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT score, std_score
        FROM Runs
        WHERE score IS NOT NULL
        ''')
        scores = cursor.fetchall()
    return [s[0] for s in scores]

def plot_runtime_vs_accuracy(top_experiments):
    """Plots runtime vs. accuracy with error bars for the top experiments."""
    experiment_names = [exp[1] for exp in top_experiments]
    scores = [exp[2] for exp in top_experiments]
    std_scores = [exp[3] for exp in top_experiments]
    durations = [exp[4] for exp in top_experiments]

    plt.figure(figsize=(10, 6))
    plt.errorbar(durations, scores, yerr=std_scores, fmt='o', capsize=5)
    plt.title('Runtime vs. Accuracy for Top Experiments')
    plt.xlabel('Runtime (seconds)')
    plt.ylabel('Accuracy')
    plt.grid(True)

    for i, name in enumerate(experiment_names):
        plt.annotate(name, (durations[i], scores[i]), textcoords="offset points", xytext=(0,5), ha='center')

    plt.show()

def plot_score_distribution(scores):
    """Plots the distribution of scores for all experiments using KDE and adds individual score points."""
    plt.figure(figsize=(10, 6))

    # Plot the KDE
    sns.kdeplot(scores, bw_adjust=1.5, fill=True, label='KDE')

    # Plot the individual score points
    sns.scatterplot(x=scores, y=[0] * len(scores), color='red', marker='x', s=50, label='Scores', zorder=3)

    plt.title('Estimated Distribution of Scores for All Experiments with Individual Scores')
    plt.xlabel('Score')
    plt.ylabel('Density')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot experimental run results.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top experiments to plot for runtime vs. accuracy.")

    args = parser.parse_args()

    # Fetch top experiments and all scores
    top_experiments = fetch_top_experiments(db_path=args.db_path, top_n=args.top_n)
    all_scores = fetch_all_scores(db_path=args.db_path)

    # Plot runtime vs. accuracy for top experiments
    plot_runtime_vs_accuracy(top_experiments)

    # Plot the distribution of scores for all experiments
    plot_score_distribution(all_scores)
