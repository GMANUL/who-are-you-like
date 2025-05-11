from PIL import Image
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet
from utils.name_by_id import NameById

class FaceService:
    def __init__(self):
        self.embeddings = Embeddings("C:\\face_dataset\\new_embeddings.npz")
        self.name_util = NameById(df_path="C:\\face_dataset\\celeb_names.csv")
        self.facenet = FaceNet()

    def get_match_list(self, image: Image.Image) -> list:
        face_embedding = self.facenet.get_embedding(image)
        top_indices = self.embeddings.find_top_indices(face_embedding)
        match_list = []
        for id in top_indices:
            celeb_name = self.name_util.get_celebrity_name(id)
            match_list.append({
                "id": id,
                "name": celeb_name
            })
        return match_list