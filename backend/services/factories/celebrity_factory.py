from PIL import Image

from repositories.db.celeb_repository import CelebRepository
from utils.facenet_utils import FaceNet
from utils.save_photo_utils import save_photo
from utils.embedding_utils import Embeddings


class CelebrityFactory:

    def __init__(
        self, 
        celeb_repository: CelebRepository,
        facenet: FaceNet,
        embeddings: Embeddings
    ):
        self.celeb_repository = celeb_repository
        self.facenet = facenet
        self.embeddings = embeddings


    async def create_celebrity(self, name: str, image: Image.Image) -> None:

        prepared_photo = self.facenet.get_prepared_photo(image)
        celeb_id = await self.celeb_repository.put_name(name)
        save_photo(prepared_photo, id=celeb_id)
        
        embedding = self.facenet.get_embedding(image)
        self.embeddings.add_embedding(embedding)
        