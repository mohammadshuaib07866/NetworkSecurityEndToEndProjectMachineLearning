import os
import sys
import pymongo
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split

# load the environment variable
load_dotenv()
MONGO_DB_URL = os.getenv("MONGODB_URL")


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            logging.info("DataIngestionConfig initialized successfully.")
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            logging.info(f"Connecting to MongoDB at: {MONGO_DB_URL}")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            collection = self.mongo_client[database_name][collection_name]

            logging.info(f"Reading data from MongoDB Collection: {collection_name}")
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            logging.info(f"Shape of dataframe: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Exporting data into feature store started...")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            logging.info(f"Feature store file path: {feature_store_file_path}")

            dir_path = os.path.dirname(feature_store_file_path)
            logging.info(f"Checking or creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Saving dataframe to feature store as CSV...")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logging.info(
                f"Data successfully exported to feature store at: {feature_store_file_path}"
            )

            return dataframe

        except Exception as e:
            logging.error("Error occurred while exporting data into feature store.")
            raise NetworkSecurityException(e, sys.exc_info())

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, 
                test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train-test split successfully")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info("Exported train and test files successfully")

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_ingestion(self):
        try:
            logging.info("Reading the data from mongoDB")
            dataframe = self.export_collection_as_dataframe()

            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)

            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                tested_file_path=self.data_ingestion_config.testing_file_path
            )

            logging.info(f"Data Ingestion Completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
