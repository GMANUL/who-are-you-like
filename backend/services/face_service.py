from PIL import Image
from typing import List, TypedDict

from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet
from repositories.db.celeb_repository import CelebRepository



class MatchResult(TypedDict):
    id: int
    name: str
    distance: float


class FaceService:
    def __init__(self) -> None:
        self.embeddings = Embeddings()
        self.celeb_repository = CelebRepository()
        self.facenet = FaceNet()

    async def get_match_list(self, image: Image.Image) -> List[MatchResult]:
        face_embedding = self.facenet.get_embedding(image)
        top_indices, top_distances = self.embeddings.find_top_indices(face_embedding)
        match_list = []
        for id, distance in zip(top_indices, top_distances):
            celeb_name = await self.celeb_repository.get_name(id)
            match_list.append({
                "id": id,
                "name": celeb_name,
                "distance": distance
            })
        return match_list

