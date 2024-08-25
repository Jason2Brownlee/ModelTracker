# Customize functions in this file

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

def load_dataset():
    """
    Loads the dataset. Returns the Iris dataset by default.
    This function can be customized to load other datasets if needed.
    """
    data = load_iris()
    X, y = data.data, data.target
    return X, y

def default_resampling_method(X, y):
    """
    Default resampling method: cross-validation with 5 folds.
    This function can be customized to use different resampling methods.
    """
    return cross_val_score, {'cv': 5}

def default_evaluation_metric():
    """
    Default evaluation metric: accuracy score.
    This function can be customized to use different evaluation metrics.
    """
    return 'accuracy'
