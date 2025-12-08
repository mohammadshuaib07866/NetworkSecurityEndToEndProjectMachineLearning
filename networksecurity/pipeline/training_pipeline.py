import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)


class TrainingPipeline:
    def __init__(self):
        try:
            # Main training pipeline configuration
            self.training_pipeline_config = TrainingPipelineConfig()
            logging.info("TrainingPipelineConfig created successfully.")

            # Data Ingestion config
            self.data_ingestion_config = DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            logging.info("DataIngestionConfig created successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    # ----------------------------------------------------
    # 1. DATA INGESTION
    # ----------------------------------------------------
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Starting Data Ingestion process...")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info(
                f"Data Ingestion Completed Successfully. Artifact: {data_ingestion_artifact}"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    # ----------------------------------------------------
    # 2. DATA VALIDATION
    # ----------------------------------------------------
    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=data_validation_config,
            )

            logging.info("Initiating Data Validation...")
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data Validation Completed Successfully.")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    # ----------------------------------------------------
    # 3. DATA TRANSFORMATION
    # ----------------------------------------------------
    def start_data_transformation(
        self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        try:
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            data_transformation = DataTransformation(
                data_validation_artifact=data_validation_artifact,
                data_transformation_config=data_transformation_config,
            )

            logging.info("Initiating Data Transformation...")
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )

            logging.info("Data Transformation Completed Successfully.")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    def start_model_trainer(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=model_trainer_config,
            )

            logging.info("Initiating Model Training...")
            model_trainer_artifact = model_trainer.initiate_model_trainer()

            logging.info("Model Training Completed Successfully.")
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())

    # ----------------------------------------------------
    # 4. RUN PIPELINE
    # ----------------------------------------------------
    def run_pipeline(self):
        try:
            logging.info("Pipeline Execution Started...")

            # Step 1: Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

            # Step 2: Validation
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )

            # Step 3: Transformation
            data_transformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            logging.info("Pipeline Execution Completed Successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
