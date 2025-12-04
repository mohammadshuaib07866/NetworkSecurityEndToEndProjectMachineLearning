from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.logger.logging import logging
from networksecurity.exception.exception import NetworkSecurityException
import sys

if __name__ == "__main__":
    try:
        logging.info("Training Pipeline started...")

        pipeline = TrainingPipeline()
        pipeline.run_pipeline()

        logging.info("Training Pipeline completed successfully.")

    except Exception as e:
        logging.error("Error occurred while running Training Pipeline.")
        raise NetworkSecurityException(e, sys.exc_info())
