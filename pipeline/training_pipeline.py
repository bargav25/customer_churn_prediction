from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_config_file
from config.paths_config import *
from config.model_params import *
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)


if __name__ == "__main__":

    try:

        config = read_config_file(CONFIG_PATH)

        data_ingestion = DataIngestion(config)
        data_ingestion.run()

        data_preprocessing = DataProcessor(TRAIN_DATA_PATH, TEST_DATA_PATH, PROCESSED_DATA_DIR,  CONFIG_PATH)
        data_preprocessing.process()

        model_training = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH, CONFIG_PATH)
        model_training.run()

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise CustomException(f"Error occurred: {e}")