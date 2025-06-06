from PIL import Image

from repositories.db.celeb_repository import CelebRepository
from utils.facenet_utils import FaceNet, MobileNet
from utils.save_photo_utils import save_photo
from utils.embedding_utils import Embeddings


class CelebrityFactory:

    def __init__(
        self, 
        celeb_repository: CelebRepository,
        facenet: FaceNet,
        mobilenet: MobileNet,
        facenet_embeddings: Embeddings,
        mobilenet_embeddings: Embeddings,

    ):
        self.celeb_repository = celeb_repository
        self.facenet = facenet
        self.mobilenet = mobilenet
        self.facenet_embeddings = facenet_embeddings
        self.mobilenet_embediings = mobilenet_embeddings


    async def create_celebrity(self, name: str, image: Image.Image) -> None:

        prepared_photo = self.facenet.get_prepared_photo(image)
        celeb_id = await self.celeb_repository.put_name(name)
        save_photo(prepared_photo, id=celeb_id)
        
        facenet_emb = self.facenet.get_embedding(image)
        self.facenet_embeddings.add_embedding(facenet_emb)

        mobilenet_emb = self.mobilenet.get_embedding(image)
        self.mobilenet_embeddings.add_embedding(mobilenet_emb)
        