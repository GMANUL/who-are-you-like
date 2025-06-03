from PIL import Image

from .base import AddCelebrityHandler
from .exceptions import NameAlreadyExistsError
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet


class EmbeddingCheckHandler(AddCelebrityHandler):

    def __init__(self, facenet: FaceNet, embeddings: Embeddings, next_handler=None):
        super().__init__(next_handler)
        self.facenet = facenet
        self.embeddings = embeddings


    async def handle(self, name: str, image: Image.Image) -> None:

        celeb_embedding = self.facenet.get_embedding(image)
        _, top_distances = self.embeddings.find_top_indices(celeb_embedding, top_k=1)

        if top_distances[0] > 0.75:
            raise NameAlreadyExistsError("Фото слишком похоже на существующую знаменитость.")
        await super().handle(name, image)