import os
import numpy as np
import faiss

class Embeddings:
    def __init__(self, npz_path: str):
        self.embeddings = self.load_embeddings(npz_path)
        self.faiss_index = self.create_faiss_index()
        self.embedding_index = self.get_embedding_index()
    
    def load_embeddings(self, path: str) -> dict:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Embedding file {path} not found")
        saved_data = np.load(path)
        embeddings = dict(zip(saved_data['names'], saved_data['embeddings']))
        return embeddings
    
    def create_faiss_index(self) -> faiss.IndexFlatIP:
        embedding_matrix = np.stack(list(self.embeddings.values())).astype('float32')
        faiss.normalize_L2(embedding_matrix)
        embedding_dim = embedding_matrix.shape[1]
        index = faiss.IndexFlatIP(embedding_dim)
        index.add(embedding_matrix)
        return index
    
    def get_embedding_index(self) -> list:
        return list(int(name) for name in self.embeddings.keys())
    
    def find_top_indices(self, embedding: np.ndarray, top_k: int = 5) -> list:
        
        faiss.normalize_L2(embedding)
        Distance, FaissIndex = self.faiss_index.search(embedding, top_k)
        embedding_indices = list(self.embedding_index[i] for i in FaissIndex[0])
        return embedding_indices