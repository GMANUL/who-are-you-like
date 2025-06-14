from PIL import Image
from typing import List

from services.handlers import(
    ExactNameCheckHandler,
    FuzzyNameCheckHandler,
    EmbeddingCheckHandler,
    SaveCelebrityHandler,
    ActionConfirmationRequired
)
from .factories.celebrity_factory import CelebrityFactory
from repositories.db.celeb_repository import CelebRepository
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet, MobileNet
from settings.settings import settings


class PersonService:

    def __init__(self, use_mobilenet: bool = False) -> None:    
        self.celeb_repository = CelebRepository()
        self.facenet = FaceNet()
        self.facenet_embeddings = Embeddings(settings.paths.facenet_emb)
        self.use_mobilenet = use_mobilenet

        if self.use_mobilenet:
            self.mobilenet = MobileNet()
            self.mobilenet_embeddings = Embeddings(settings.paths.mobilenet_emb)

        self.celebrity_factory = CelebrityFactory(
            celeb_repository = self.celeb_repository, 
            facenet = self.facenet, 
            facenet_embeddings = self.facenet_embeddings,
            mobilenet = self.mobilenet if self.use_mobilenet else None,
            mobilenet_embeddings = self.mobilenet_embeddings if self.use_mobilenet else None
        )

        self._create_chains()

    
    def _create_chains(self):

        self.add_celebrity_chain = self._build_full_chain()
        self.force_add_celebrity_chain = self._build_force_chain()


    def _build_full_chain(self):

        chain = SaveCelebrityHandler(self.celebrity_factory)
        chain = EmbeddingCheckHandler(self.facenet, self.facenet_embeddings, chain)

        if self.use_mobilenet:
            chain = EmbeddingCheckHandler(self.mobilenet, self.mobilenet_embeddings, chain)
        
        chain = FuzzyNameCheckHandler(self.celeb_repository, chain)
        chain = ExactNameCheckHandler(self.celeb_repository, chain)
        return chain


    def _build_force_chain(self):

        chain = SaveCelebrityHandler(self.celebrity_factory)
        chain = EmbeddingCheckHandler(self.facenet, self.facenet_embeddings, chain)

        if self.use_mobilenet:
            chain = EmbeddingCheckHandler(self.mobilenet, self.mobilenet_embeddings, chain)

        return chain


    async def add_celebrity(self, name: str, image: Image.Image, force: bool) -> None:

        if force:
            await self.force_add_celebrity_chain.handle(name, image)
        else:
            await self.add_celebrity_chain.handle(name, image)
    

    async def get_similar_names(self, query: str) -> List[str]:
        
        return await self.celeb_repository.name_search(query)
    