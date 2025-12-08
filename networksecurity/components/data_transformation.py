import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.constant import *
from networksecurity.entity.config_entity import (
    DataValidationConfig,
    DataTransformationConfig,
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
from networksecurity.utils.common import save_numpy_array_data, save_object


class DataTransformation:
    def __init__(
        self,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_config: DataTransformationConfig,
    ):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def get_data_transformed_object(self) -> Pipeline:
        try:
            logging.info("Entered get_data_transformed_object method")

            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            preprocessor = Pipeline([("imputer", imputer)])
            return preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method")
        try:
            logging.info("Reading train and test files")

            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            logging.info("Data read successfully")

            # Split input/output features
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # Preprocessing
            preprocessor = self.get_data_transformed_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)

            transformed_input_train = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test = preprocessor_object.transform(input_feature_test_df)

            # Combine input + output
            train_arr = np.c_[transformed_input_train, target_feature_train_df]
            test_arr = np.c_[transformed_input_test, target_feature_test_df]

            # Save train/test arrays
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )

            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )

            # Save preprocessor object
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )
            save_object("final_model/preprocessing.pkl",preprocessor)

            # Prepare artifact
            artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )

            logging.info("Data Transformation Completed Successfully.")
            return artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
