import os
import sys
import numpy as np
import pandas as pd


"""
Defining common constant variable for training pipeline

"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "networksecuritypipeline"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phisingdata.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

"""
Data Ingestion related constant start with data_ingestion VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "data"
DATA_INGESTION_DATABASE_NAME: str = "networksecuritydata"
DATA_INTESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"

# Fixed missing "="
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


"""
Data Transformation related constant start With DATA_TRANSFORMATION VAR NAME

"""
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"

DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbours": 3,
    "weights": "uniform",
}


DATA_TRANSFORMATON_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"
