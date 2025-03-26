import os
import yaml
from src.logger import get_logger
from src.custom_exception import CustomException
import pandas as pd

logger = get_logger(__name__)

def read_config_file(config_path):
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found in path: {config_path}")
        
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            logger.info(f"Config file loaded successfully from path: {config_path}")
            return config

    except Exception as e:
        logger.error("Error occurred while reading config file {config_path}")
        raise CustomException(f"Error occurred while reading config file {config_path}: {e}")
    
def load_data(path):
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Data file not found in path: {path}")
        
        data = pd.read_csv(path)
        logger.info(f"Data loaded successfully from path: {path}")
        return data
        
    except Exception as e:
        logger.error("Error occurred while loading data {path}")
        raise CustomException(f"Error occurred while loading data {path}: {e}")
    
def make_categorical(data: pd.DataFrame, column: str, categories: list, ordered: bool = False):
    data[column] = pd.Categorical(data[column], categories=categories, ordered=ordered)
    data[column] = data[column].cat.codes
    return data