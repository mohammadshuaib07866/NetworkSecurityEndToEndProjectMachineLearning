import os
import sys
from datetime import datetime
from networksecurity.constants.constant import *


class TrainingPipelineConfig:
    def __init__(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now()

        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

        self.pipeline_name = PIPELINE_NAME
        self.artifact_name = ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.model_dir = os.path.join("final_model")
        self.timestamp = timestamp


class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):

        # Data ingestion main folder → artifacts/<timestamp>/data_ingestion
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            DATA_INTESTION_DIR_NAME
        )

        # Feature store file path
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            DATA_INGESTION_FEATURE_STORE_DIR,
            FILE_NAME
        )

        # Train-test split output folder
        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            DATA_INGESTED_DIR,
            TRAIN_FILE_NAME
        )

        self.testing_file_path = os.path.join(
            self.data_ingestion_dir,
            DATA_INGESTED_DIR,
            TEST_FILE_NAME
        )

        # Other settings
        self.train_test_split_ratio = DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name = DATA_INGESTION_COLLECTION_NAME
        self.database_name = DATA_INGESTION_DATABASE_NAME
