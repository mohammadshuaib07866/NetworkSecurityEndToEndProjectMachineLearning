import os, sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")


project_name = "networksecurity"

list_of_files = [
    ".github/workflows/.gitkeep",
    "data/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/cloud/__init__.py",
    f"{project_name}/cloud/cloud_s3_syncer.py",
    f"{project_name}/cloud/s3_syncer.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/constants/common.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/logger/logging.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/exception/exception.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/batch_prediction.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/metric/__init__.py",
    f"{project_name}/utils/metric/classification_metric.py",
    f"{project_name}/utils/model/__init__.py",
    f"{project_name}/utils/model/estimator.py",
    f"{project_name}/utils/common.py",
    "notebooks/eda.ipynb",
    "notebooks/model_training.ipynb",
    "prediction.ipynb",
    "valid_data/.gitkeep",
    "data_schema/schema.yaml",
    "app.py",
    "main.py",
    "push_data.py",
    "Dockerfile",
]


for file in list_of_files:
    filepath = Path(file)
    filedir, filename = os.path.split(filepath)

    # Creating directory if it does not exists
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory Created: {filedir}")

    # Create file if it does not exists
    if (not filepath.exists()) or filepath.stat().st_size() == 0:
        with open(filepath, "w") as f:
            pass
        logging.info(f"File Created: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
