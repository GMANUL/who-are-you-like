from typing import List, Optional, TypedDict
import torch

from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceEmbedder
from repositories.db.celeb_repository import CelebRepository


class MatchResult(TypedDict):
    id: int
    name: str
    distance: float


class EmbeddingHandler:

    def __init__(
        self,
        model: FaceEmbedder,
        embeddings: Embeddings,
        celeb_repository: CelebRepository,
        similarity_threshold: float = 0.5,
        next_handler: Optional['EmbeddingHandler'] = None,
    ):
        self.model = model
        self.embeddings = embeddings
        self.celeb_repository = celeb_repository
        self.similarity_threshold = similarity_threshold
        self.next_handler = next_handler


    def _is_good_match(self, matches: List[MatchResult]) -> bool:
        return any(match["distance"] > self.similarity_threshold for match in matches)


    async def get_match_list(self, cropped_image_tensor: torch.tensor) -> List[MatchResult]:

        face_embedding = self.model.get_embedding(cropped_image_tensor)
        top_indices, top_distances = self.embeddings.find_top_indices(face_embedding)

        match_list = []
        for id, distance in zip(top_indices, top_distances):
            celeb_name = await self.celeb_repository.get_name(id)
            match_list.append({"id": id, "name": celeb_name, "distance": distance})

        if self._is_good_match(match_list):
            return match_list
        elif self.next_handler:
            return await self.next_handler.get_match_list(cropped_image_tensor)
        else:
            return match_list
