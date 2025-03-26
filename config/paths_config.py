import os

######### DATA INGESTION #########

RAW_DATA_DIR = "artifacts/raw"

RAW_DATA_PATH = os.path.join(RAW_DATA_DIR, "data.csv")
TRAIN_DATA_PATH = os.path.join(RAW_DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(RAW_DATA_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"



######### DATA PROCESSING #########

PROCESSED_DATA_DIR = "artifacts/processed"
PROCESSED_TRAIN_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "train.csv")
PROCESSED_TEST_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "test.csv")

########## MODEL TRAINING #########

MODEL_OUTPUT_PATH = "artifacts/models/model.pkl"

