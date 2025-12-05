from networksecurity.entity.artifact_entity import (
    DataValidationArtifact,
    DataIngestionArtifact,
)
from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from networksecurity.constants.constant import *
from networksecurity.utils.common import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required columns: {number_of_columns}")
            logging.info(f"Dataset columns: {len(dataframe.columns)}")

            return len(dataframe.columns) == number_of_columns

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            drift_status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]

                test_result = ks_2samp(d1, d2)
                p_value = float(test_result.pvalue)

                drift_detected = p_value < threshold
                if drift_detected:
                    drift_status = False

                report[column] = {
                    "p_value": p_value,
                    "drift_detected": drift_detected,
                }

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(drift_report_file_path, report, replace=True)

            return drift_status

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_path = self.data_ingestion_artifact.trained_file_path
            test_path = self.data_ingestion_artifact.tested_file_path

            train_df = self.read_data(train_path)
            test_df = self.read_data(test_path)

            # Column validation
            if not self.validate_number_of_columns(train_df):
                raise NetworkSecurityException("Train dataset column mismatch", sys.exc_info())

            if not self.validate_number_of_columns(test_df):
                raise NetworkSecurityException("Test dataset column mismatch", sys.exc_info())

            # Detect drift
            drift_status = self.detect_dataset_drift(train_df, test_df)

            # Save validated files
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)

            # Create artifact object
            data_validation_artifact = DataValidationArtifact(
                validation_status=drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
