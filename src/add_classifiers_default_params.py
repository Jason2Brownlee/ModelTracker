# add all main sklearn classifiers with default hyperparameters


from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from experiment_manager import ExperimentManager

# List of classifiers with their names
classifiers = {
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
    "SVM": SVC(),
    "K-Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": GaussianNB()
}

def add_classification_experiments(db_path):
    manager = ExperimentManager(db_path)

    for name, clf in classifiers.items():
        # Optionally wrap the classifier in a pipeline with a scaler
        pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Add scaling as a preprocessing step
            ('classifier', clf)
        ])

        # Add the experiment to the database
        manager.add_experiment(
            experiment_name=name,
            model=pipeline,
            config=clf.get_params(),
            description=f"Default {name} classifier with StandardScaler"
        )

if __name__ == "__main__":
    db_path = "data/experiments.db"  # Path to your database
    add_classification_experiments(db_path)
    print("All classification experiments added successfully.")
