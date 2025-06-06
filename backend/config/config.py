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

DB_PATH='data/sqlite_imdb.db'
APP_PATH='/app'
DATASET_NAME='imdb_dataset'
NAME_LIST_FILE='celeb_names.txt'
FACENET_EMBEDDINGS_FILE='embeddings.faiss'
MOBILENET_EMBEDDINGS_FILE='mobile_embeddings.faiss'
IMAGES_DIR='celeb_images'
FACENET_MODEL_WEIGHTS='/weights/facenet-torch/20180402-114759-vggface2.pt'
MOBILENET_MODEL_WEIGHTS='/weights/mobilenet-v3/mobilenet_v3_small.pth'
