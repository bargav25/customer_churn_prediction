import os
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import load_data, read_config_file
from sklearn.model_selection import RandomizedSearchCV

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:

    def __init__(self, train_path, test_path, model_output_path, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path
        self.config = read_config_file(config_path)

        self.params_dict = LIGHTGBM_PARAMS
        self.search_params = SEARCH_PARAMS

    def load_data(self):

        try:

            logger.info("Loading data")

            self.config = self.config['data_processing']


            train_data = load_data(self.train_path)
            test_data = load_data(self.test_path)

            X_train = train_data.drop(columns=[self.config['target_column']])
            y_train = train_data[self.config['target_column']]

            X_test = test_data.drop(columns=[self.config['target_column']])
            y_test = test_data[self.config['target_column']]

            logger.info("Data loaded successfully")

            return X_train, X_test, y_train, y_test
        
        except Exception as e:
            logger.error(f"Error occurred while loading data: {e}")
            raise CustomException(f"Error occurred while loading data: {e}")
        
    def train_model(self, X_train, y_train):

        try:

            logger.info("Initializing the model")

            model = lgb.LGBMClassifier(random_state = self.search_params['random_state'])

            logger.info("Starting hyperparameter tuning")

            random_search = RandomizedSearchCV(model, param_distributions=self.params_dict, **self.search_params)

            random_search.fit(X_train, y_train)

            logger.info("Hyperparameter tuning completed")

            best_params = random_search.best_params_
            best_model = random_search.best_estimator_

            logger.info("Best parameters: ", best_params)

            return best_model

        except Exception as e:
            logger.error(f"Error occurred while training model: {e}")
            raise CustomException(f"Error occurred while training model: {e}")
        
    def evaluate_model(self, model, X_test, y_test):

        try:

            logger.info("Evaluating model")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info("Model evaluation completed")

            logger.info(f"Accuracy: {accuracy}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"F1: {f1}")

            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1
            }

        except Exception as e:
            logger.error(f"Error occurred while evaluating model: {e}")
            raise CustomException(f"Error occurred while evaluating model: {e}")
        
    def save_model(self, model):
        
        try:

            logger.info("Saving model")

            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            joblib.dump(model, self.model_output_path)

            logger.info("Model saved successfully to path: ", self.model_output_path)

        except Exception as e:
            logger.error(f"Error occurred while saving model: {e}")
            raise CustomException(f"Error occurred while saving model: {e}")
        
    def run(self):

        try:

            with mlflow.start_run():

                mlflow.log_artifact(self.train_path, "datasets")
                mlflow.log_artifact(self.test_path, "datasets")

                X_train, X_test, y_train, y_test = self.load_data()

                model = self.train_model(X_train, y_train)

                model_evaluation = self.evaluate_model(model, X_test, y_test)

                self.save_model(model)

                mlflow.log_artifact(self.model_output_path)

                mlflow.log_params(model.get_params())
                mlflow.log_metrics(model_evaluation)

                return model_evaluation

        except Exception as e:
            logger.error(f"Error occurred in training pipeline: {e}")
            raise CustomException(f"Error occurred in training pipeline: {e}")
        
if __name__ == "__main__":
    model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH, CONFIG_PATH)
    model_training.run()