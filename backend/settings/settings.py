import os

from pydantic_settings import BaseSettings
from config.config import DB_PATH, APP_PATH, DATASET_NAME, NAME_LIST_FILE, EMBEDDINGS_FILE, IMAGES_DIR, EMBEDDING_MODEL_WEIGHTS


class Paths():
    database: str = os.path.join(APP_PATH, DB_PATH)
    name_list: str = os.path.join(APP_PATH, DATASET_NAME, NAME_LIST_FILE)
    embeddings: str = os.path.join(APP_PATH, DATASET_NAME, EMBEDDINGS_FILE)
    images_dir: str = os.path.join(APP_PATH, DATASET_NAME, IMAGES_DIR)
    embedding_model: str = EMBEDDING_MODEL_WEIGHTS


class _Settings(BaseSettings):
    paths: Paths = Paths()


settings = _Settings()