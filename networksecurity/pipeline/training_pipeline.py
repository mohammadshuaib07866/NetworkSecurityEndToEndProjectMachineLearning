import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact


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

    def run_pipeline(self):
        try:
            logging.info("Pipeline Execution Started...")
            data_ingestion_artifact = self.start_data_ingestion()
            logging.info("Pipeline Execution Completed Successfully.")

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
