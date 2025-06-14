import os
import multiprocessing as mp
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from config.config import DB_PATH, APP_PATH, DATASET_NAME, NAME_LIST_FILE, FACENET_EMBEDDINGS_FILE, IMAGES_DIR, \
    FACENET_MODEL_WEIGHTS, MOBILENET_EMBEDDINGS_FILE, MOBILENET_MODEL_WEIGHTS


class Paths(BaseModel):
    database: str = os.path.join(APP_PATH, DB_PATH)
    name_list: str = os.path.join(APP_PATH, DATASET_NAME, NAME_LIST_FILE)
    facenet_emb: str = os.path.join(APP_PATH, DATASET_NAME, FACENET_EMBEDDINGS_FILE)
    mobilenet_emb: str = os.path.join(APP_PATH, DATASET_NAME, MOBILENET_EMBEDDINGS_FILE)
    images_dir: str = os.path.join(APP_PATH, DATASET_NAME, IMAGES_DIR)
    facenet_model: str = FACENET_MODEL_WEIGHTS
    mobilenet_model: str = MOBILENET_MODEL_WEIGHTS


class Uvicorn(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = mp.cpu_count() * 2 + 1


class _Settings(BaseSettings):
    paths: Paths = Paths()
    uvicorn: Uvicorn = Uvicorn()


settings = _Settings()