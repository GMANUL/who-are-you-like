"""
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = str(os.getenv('DB_PATH'))
APP_PATH = str(os.getenv('APP_PATH'))
DATASET_NAME = str(os.getenv('DATASET_NAME'))
NAME_LIST_FILE = str(os.getenv('CELEB_NAME_LIST'))
EMBEDDINGS_FILE = str(os.getenv('EMBEDDINGS_FILE'))
IMAGES_DIR = str(os.getenv('IMAGES_DIR'))
"""

DB_PATH='data/sqlite_tiny.db'
APP_PATH='/app'
DATASET_NAME='tiny_dataset'
NAME_LIST_FILE='celeb_names_tiny.txt'
EMBEDDINGS_FILE='tiny_embeddings.faiss'
IMAGES_DIR='tiny_imdb'
EMBEDDING_MODEL_WEIGHTS='/weights/facenet-torch/20180402-114759-vggface2.pt'
