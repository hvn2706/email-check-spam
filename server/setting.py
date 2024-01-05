import os

from pydantic.v1 import BaseSettings


class Setting(BaseSettings):
    ROOT_DIR = os.path.abspath(os.path.join(
        os.path.dirname(__file__)
    ))
    ENV: str = os.getenv('ENV', '')
    EMBEDDING_MODEL_PATH: str = os.getenv('EMBEDDING_MODEL_PATH', 'prediction_models/tfidf_transformer.sav')
    SPAM_EMAIL_DETECTION_MODEL_PATH: str = os.getenv('SPAM_EMAIL_DETECTION_MODEL_PATH',
                                                     'prediction_models/svm_tfidf_model.sav')


setting = Setting()
