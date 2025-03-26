import os
import pandas as pd
import numpy as np
from google.cloud import storage
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_config_file
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

class DataIngestion:

    def __init__(self, config):

        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["file_name"]
        self.test_size = self.config["test_size"]
        self.random_state = self.config["random_state"]

        os.makedirs(RAW_DATA_DIR, exist_ok=True)

        logger.info(f"Data Ingestion start with the bucket {self.bucket_name} and file {self.file_name}")

    def get_data_from_gcs(self):

        try:

            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_DATA_PATH)

            logger.info(f"Data downloaded from GCS to {RAW_DATA_PATH}")

        except Exception as e:
            
            logger.error(f"Error in downloading the data from GCS: {e}")
            raise CustomException(f"Error in downloading the data from GCS: {e}")
        
    def split_data(self):

        try:

            data = pd.read_csv(RAW_DATA_PATH)

            train, test = train_test_split(data, test_size=self.test_size, random_state=self.random_state)

            train.to_csv(TRAIN_DATA_PATH, index=False)
            test.to_csv(TEST_DATA_PATH, index=False)

            logger.info(f"Data split into train and test and saved at {TRAIN_DATA_PATH} and {TEST_DATA_PATH}")

        except Exception as e:
            
            logger.error(f"Error in splitting the data: {e}")
            raise CustomException(f"Error in splitting the data: {e}")
        
    def run(self):

        try:
            self.get_data_from_gcs()
            self.split_data()
        except CustomException as e:
            logger.error(f"CustomException: {e}")
        finally:
            logger.info("Data Ingestion completed")

if __name__ == "__main__":

    config = read_config_file(CONFIG_PATH)
    
    data_ingestion = DataIngestion(config)
    data_ingestion.run()








