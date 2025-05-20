from PIL import Image
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet
from utils.name_by_id import NameById
import os

class FaceService:
    def __init__(self):
        self.embeddings = Embeddings(os.path.join("/app", "celeb_data", "new_embeddings.npz"))
        self.name_util = NameById(os.path.join("/app", "celeb_data", "celeb_names.csv"))
        self.facenet = FaceNet()

    def get_match_list(self, image: Image.Image) -> list:
        face_embedding = self.facenet.get_embedding(image)
        top_indices, top_distances = self.embeddings.find_top_indices(face_embedding)
        match_list = []
        for id, distance in zip(top_indices, top_distances):
            celeb_name = self.name_util.get_celebrity_name(id)
            match_list.append({
                "id": id,
                "name": celeb_name,
                "distance": distance
            })
        return match_list