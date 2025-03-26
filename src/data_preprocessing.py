import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_config_file, load_data, make_categorical
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE


logger = get_logger(__name__)

class DataProcessor:

    def __init__(self, train_path, test_path, processed_dir, config_path):

        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_config_file(config_path)
        self.config = self.config["data_processing"]

        os.makedirs(self.processed_dir, exist_ok=True)

        logger.info(f"Data Processing started with train path: {self.train_path}, test path: {self.test_path} and processed dir: {self.processed_dir}")

    def preprocess_data(self, df):

        try:

            logger.info("Data Preprocessing started")

            logger.info("Dropping columns")
            df = df.drop(self.config["drop_columns"], axis=1)

            logger.info("Converting categorical columns")
            ordinal_config = self.config["ordinal_encoding"]
            for column, categories in ordinal_config.items():
                df = make_categorical(df, column, categories, ordered=True)

            logger.info("Binary encoding columns")
            binary_config = self.config["binary_encoding"]
            for column, mapping in binary_config.items():
                df[column] = df[column].replace(mapping)

            logger.info("Data Preprocessing completed")

            return df

        except Exception as e:
            logger.error(f"Error in data preprocessing: {e}")
            raise CustomException(f"Error in data preprocessing: {e}")
        
    def balance_data(self, df):

        try:

            logger.info("Data Balancing started")

            X = df.drop(self.config["target_column"], axis=1)
            y = df[self.config["target_column"]]

            smote = SMOTE(random_state=42)
            X_res, y_res = smote.fit_resample(X, y)

            df = pd.concat([X_res, y_res], axis=1)

            logger.info("Data Balancing completed")

            return df

        except Exception as e:
            logger.error(f"Error in data balancing: {e}")
            raise CustomException(f"Error in data balancing: {e}")

    def select_features(self, df):

        try:

            num_features = self.config["num_top_features"]
            target = self.config["target_column"]

            X, y = df.drop(target, axis=1), df[target]

            clf = RandomForestClassifier(random_state=42)

            clf.fit(X, y)

            importances = clf.feature_importances_
            indices = np.argsort(importances)[::-1]

            top_features = X.columns[indices][:num_features]

            df = df[top_features.tolist() + [target]]

            logger.info(f"Selected top {num_features} features successfully")

            return df
        
        except Exception as e:
            logger.error(f"Error in feature selection: {e}")
            raise CustomException(f"Error in feature selection: {e}")
        
    
    def save_data(self, df, path):

        try:

            df.to_csv(path, index=False)
            logger.info(f"Data saved successfully at {path}")

        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise CustomException(f"Error in saving data: {e}")
        
    def process(self):

        try:

            train = load_data(self.train_path)
            test = load_data(self.test_path)

            train = self.preprocess_data(train)
            test = self.preprocess_data(test)

            train = self.balance_data(train)

            train = self.select_features(train)
            test = test[train.columns]

            self.save_data(train, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test, PROCESSED_TEST_DATA_PATH)

            logger.info("Data Processing completed")

        except CustomException as e:
            logger.error(f"CustomException: {e}")

if __name__ == "__main__":
    
    processor = DataProcessor(TRAIN_DATA_PATH, TEST_DATA_PATH, PROCESSED_DATA_DIR, CONFIG_PATH)
    processor.process()



        


            



            







