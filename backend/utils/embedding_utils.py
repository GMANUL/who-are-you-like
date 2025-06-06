import os
import numpy as np
import faiss
import signal
import time
from typing import Dict, Tuple, List
from threading import Thread
from settings.settings import settings


class Embeddings:

    _instances: Dict[str, 'Embeddings'] = {}
    _initialized_flags: Dict[str, bool] = {}

    def __new__(cls, faiss_path: str):

        if faiss_path not in cls._instances:
            cls._instances[faiss_path] = super().__new__(cls)
        return cls._instances[faiss_path]


    def __init__(self, faiss_path: str) -> None:

        if not self._initialized_flags.get(faiss_path, False):
            self.faiss_path = faiss_path
            self.loaded_index = self.load_faiss_index(self.faiss_path)
            
            signal.signal(signal.SIGTERM, self.handle_termination)
            self.last_modified = False
            
            self._saver_thread = Thread(target=self._background_saver, daemon=True)
            self._saver_thread.start()
            
            self._initialized_flags[faiss_path] = True


    def handle_termination(self, signum, frame) -> None:

        self.auto_save()
        os._exit(0)
    

    def _background_saver(self) -> None:

        while True:
            time.sleep(600)
            self.auto_save()
    

    def auto_save(self) -> None:

        if self.last_modified:
            self._save()
    

    def _save(self) -> None:
        
        temp_path = f"{self.faiss_path}.tmp"
        faiss.write_index(self.loaded_index, temp_path)
        os.replace(temp_path, self.faiss_path)
        self.last_modified = False
    

    def load_faiss_index(self, path: str) -> faiss.IndexFlatIP:

        index = faiss.read_index(path)
        return index
    

    def add_embedding(self, embedding: np.ndarray) -> None:

        faiss.normalize_L2(embedding)
        self.loaded_index.add(embedding)
        self.last_modified = True
    
     
    def find_top_indices(self, embedding: np.ndarray, top_k: int = 5) -> Tuple[List[int], List[float]]:

        faiss.normalize_L2(embedding)
        Distance, FaissIndex = self.loaded_index.search(embedding, top_k)
        top_indices = list(int(i) for i in FaissIndex[0])
        top_distances = Distance[0].tolist()
        return top_indices, top_distances