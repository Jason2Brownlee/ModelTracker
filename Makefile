# Variables
PYTHON = python3
SRC_DIR = src
DATA_DIR = data
DB_NAME = experiments.db

# Default target
all: run-experiments

# Target to create the database
create-database:
	$(PYTHON) $(SRC_DIR)/create_database.py $(DATA_DIR)/$(DB_NAME)

# Target to add a sample experiment
add-experiments:
# 	$(PYTHON) $(SRC_DIR)/experiment_manager.py
	$(PYTHON) $(SRC_DIR)/add_classifiers_default_params.py

# Target to run pending experiments
run-experiments:
	$(PYTHON) $(SRC_DIR)/run_experiments.py $(DATA_DIR)/$(DB_NAME)

# Target to show the top n results
show-results:
	$(PYTHON) $(SRC_DIR)/report_top_experiments.py $(DATA_DIR)/$(DB_NAME) --top_n 5

# Target to plot results
plot-scores:
	$(PYTHON) $(SRC_DIR)/plot_experiment_results.py $(DATA_DIR)/$(DB_NAME) --top_n 3

# Target to fit the final model
final-model:
	$(PYTHON) $(SRC_DIR)/fit_final_model.py $(DATA_DIR)/$(DB_NAME) 1

# Clean the database (optional target)
clean:
	rm -f $(DATA_DIR)/$(DB_NAME)

.PHONY: all create-database add-experiment run-experiments show-results plot-scores final-model clean
