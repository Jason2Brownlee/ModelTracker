# Model Tracker

Lightweight predictive modeling machine learning model tracking system.

## Summary

**ModelTracker** is a system designed to streamline the experimentation and tracking of machine learning models. It allows data scientists to record and manage their experiments by automatically storing models, configurations, and evaluation metrics in a SQLite database. The system provides robust functionality for retrieving and analyzing experimental results, including the ability to fit final models on full datasets and visualize the performance distribution across experiments. With features such as automated tracking of model performance, runtime analysis, and kernel density estimates for score distributions, this system enables efficient management and insightful analysis of machine learning workflows, ensuring reproducibility and facilitating the selection of optimal models for deployment.

Developed in collaboration with ChatGPT4o in August 2024.

## Usage

### Setup and Installation

1. **Clone the Repository**:
   Clone the GitHub repository to your local machine.

2. **Install Dependencies**:
   Ensure that you have Python 3 installed, along with the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the Database**:
   Initialize the SQLite database by running:
   ```bash
   make create-database
   ```

4. **Add Sample Experiments**:
   Add sample experiments using default classifier parameters:
   ```bash
   make add-experiments
   ```

5. **Run Experiments**:
   Execute all pending experiments:
   ```bash
   make run-experiments
   ```

6. **Show Top Results**:
   Display the top 5 experiments based on accuracy:
   ```bash
   make show-results
   ```

7. **Plot Experiment Results**:
   Visualize the runtime vs. accuracy for the top 3 models and the distribution of all scores:
   ```bash
   make plot-scores
   ```

8. **Fit the Final Model**:
   Fit a final model using the best experiment ID:
   ```bash
   make final-model
   ```

9. **Clean the Database** (optional):
   Remove the current database to start fresh:
   ```bash
   make clean
   ```

### Customization

To customize your dataset loading, resampling method, and evaluation metric, edit the `custom_config.py` file located in the `src` directory.

1. **`load_dataset()`**:
   - Purpose: Loads the dataset used for experiments.
   - Customization: Modify this function to load your specific dataset.

2. **`default_resampling_method(X, y)`**:
   - Purpose: Defines the resampling method (e.g., cross-validation) used during model evaluation.
   - Customization: Update this function to reflect your preferred resampling strategy.

3. **`default_evaluation_metric()`**:
   - Purpose: Specifies the evaluation metric (e.g., accuracy, F1 score) used to assess model performance.
   - Customization: Change this function to return the appropriate metric for your problem domain.

## TODO

* Use 10-fold repeated stratified cross validation to evaluate models as the default.
* Add a script that inserts a grid search experiments of common hyperparameters for common classifications algorithms.
* Write a script/bash snippet/make target that polls the database for top scores that can be run in a shell while experiments are running.
* Perhaps add a one-age website that gives a live review scores and plots.


