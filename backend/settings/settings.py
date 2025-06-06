import os

from pydantic_settings import BaseSettings
from config.config import DB_PATH, APP_PATH, DATASET_NAME, NAME_LIST_FILE, FACENET_EMBEDDINGS_FILE, IMAGES_DIR, \
    FACENET_MODEL_WEIGHTS, MOBILENET_EMBEDDINGS_FILE, MOBILENET_MODEL_WEIGHTS


class Paths():
    database: str = os.path.join(APP_PATH, DB_PATH)
    name_list: str = os.path.join(APP_PATH, DATASET_NAME, NAME_LIST_FILE)
    facenet_emb: str = os.path.join(APP_PATH, DATASET_NAME, FACENET_EMBEDDINGS_FILE)
    mobilenet_emb: str = os.path.join(APP_PATH, DATASET_NAME, MOBILENET_EMBEDDINGS_FILE)
    images_dir: str = os.path.join(APP_PATH, DATASET_NAME, IMAGES_DIR)
    facenet_model: str = FACENET_MODEL_WEIGHTS
    mobilenet_model: str = MOBILENET_MODEL_WEIGHTS


class _Settings(BaseSettings):
    paths: Paths = Paths()


settings = _Settings()