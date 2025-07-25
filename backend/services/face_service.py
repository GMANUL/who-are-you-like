from PIL import Image
from typing import List, TypedDict

from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet, MobileNet
from repositories.db.celeb_repository import CelebRepository
from settings.settings import settings
from services.handlers.face_matcher import EmbeddingHandler, MatchResult


class FaceService:

    def __init__(self, use_mobilenet: bool = False) -> None:
        self.celeb_repository = CelebRepository()
        self.facenet = FaceNet()
        self.facenet_embeddings = Embeddings(settings.paths.facenet_emb)
        self.use_mobilenet = use_mobilenet

        if self.use_mobilenet:
            self.mobilenet = MobileNet()
            self.mobilenet_embeddings = Embeddings(settings.paths.mobilenet_emb)


    async def get_match_list(self, image: Image.Image) -> List[MatchResult]:

        cropped_image = self.facenet.crop_face(image)

        facenet_handler = EmbeddingHandler(
            model=self.facenet,
            embeddings=self.facenet_embeddings,
            celeb_repository=self.celeb_repository,
            similarity_threshold=0.4,
        )

        if self.use_mobilenet:
            mobilenet_handler = EmbeddingHandler(
                model=self.mobilenet,
                embeddings=self.mobilenet_embeddings,
                celeb_repository=self.celeb_repository,
                similarity_threshold=0.7,
                next_handler=facenet_handler,
            )
            return await mobilenet_handler.get_match_list(cropped_image)
        else:
            return await facenet_handler.get_match_list(cropped_image)
