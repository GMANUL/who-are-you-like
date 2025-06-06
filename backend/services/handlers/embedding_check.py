from PIL import Image

from .base import AddCelebrityHandler
from .exceptions import NameAlreadyExistsError
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceEmbedder


class EmbeddingCheckHandler(AddCelebrityHandler):

    def __init__(self, model: FaceEmbedder, embeddings: Embeddings, next_handler=None):
        super().__init__(next_handler)
        self.model = model
        self.embeddings = embeddings


    async def handle(self, name: str, image: Image.Image, context: dict = None) -> None:

        context = context or {}
        
        if 'cropped_image' not in context:
            context['cropped_image'] = self.model.crop_face(image)

        celeb_embedding = self.model.get_embedding(context['cropped_image'])
        _, top_distances = self.embeddings.find_top_indices(celeb_embedding, top_k=1)

        if top_distances[0] > 0.75:
            raise NameAlreadyExistsError("Фото слишком похоже на существующую знаменитость.")
        await super().handle(name, image, context=context)