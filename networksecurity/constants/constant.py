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

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.ymal")

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
