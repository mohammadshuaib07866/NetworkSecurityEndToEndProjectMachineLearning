import os, sys
import mlflow
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.model.estimator import NetworkModel
from networksecurity.utils.common import (
    save_object,
    load_object,
    load_numpy_array_data,
    evaluate_models,
)
from networksecurity.utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)


import dagshub
dagshub.init(repo_owner='mohammadshuaib07866', repo_name='Machine-Learning-End-To-End-Project', mlflow=True)



class ModelTrainer:
    def __init__(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig,
    ):
        try:
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
    

    # ----------------------- MLflow Tracking -----------------------
    def track_mflow(self, best_model, classification_metric, best_model_name):
        try:
            tracking_url_type_store = mlflow.get_tracking_uri().split(":")[0]

            with mlflow.start_run():     # FIXED
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall", recall_score)

                # mlflow.sklearn.log_model(best_model, "model")  # FIXED

                # # Model Registry works only when backend is NOT file-store
                # if tracking_url_type_store != "file":
                #     mlflow.sklearn.log_model(
                #         best_model,
                #         "model",
                #         registered_model_name=best_model_name,
                #     )

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())


    # ----------------------- Train Model -----------------------
    def train_model(self, X_train, y_train, X_test, y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),
        }

        params = {
            "Decision Tree": {"criterion": ["gini", "entropy", "log_loss"]},
            "Random Forest": {"n_estimators": [8, 16, 32, 128, 256]},
            "Gradient Boosting": {
                "learning_rate": [0.1, 0.01, 0.05, 0.001],
                "subsample": [0.6, 0.7, 0.75, 0.85, 0.9],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
            "Logistic Regression": {},
            "AdaBoost": {
                "learning_rate": [0.1, 0.01, 0.001],
                "n_estimators": [8, 16, 32, 64, 128, 256],
            },
        }

        model_report = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            params=params,
        )

        # Best score
        best_model_score = max(model_report.values())

        # Best model name
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        # Train metrics
        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(
            y_true=y_train, y_pred=y_train_pred
        )

        # Track train run
        self.track_mflow(best_model, classification_train_metric, best_model_name)

        # Test metrics
        y_test_pred = best_model.predict(X_test)

        classification_test_metric = get_classification_score(
            y_true=y_test, y_pred=y_test_pred
        )

        # Track test run
        self.track_mflow(best_model, classification_test_metric, best_model_name)

        # Save Final Model with Preprocessor
        preprocessor = load_object(
            self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, network_model)
        save_object("final_model/model.pkl",best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
        )

        logging.info(f"Model trainer artifact: {model_trainer_artifact}")

        return model_trainer_artifact

    # ----------------------- Initiate Training -----------------------
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_train_file_path
            )
            test_arr = load_numpy_array_data(
                self.data_transformation_artifact.transformed_test_file_path
            )

            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            return self.train_model(X_train, y_train, X_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys.exc_info())
