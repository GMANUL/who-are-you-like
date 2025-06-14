from PIL import Image
from typing import Optional

from repositories.db.celeb_repository import CelebRepository
from utils.facenet_utils import FaceNet, MobileNet
from utils.save_photo_utils import save_photo
from utils.embedding_utils import Embeddings


class CelebrityFactory:

    def __init__(
        self, 
        celeb_repository: CelebRepository,
        facenet: FaceNet,
        facenet_embeddings: Embeddings,
        mobilenet: Optional[MobileNet] = None,
        mobilenet_embeddings: Optional[Embeddings] = None,
    ):
        self.celeb_repository = celeb_repository
        self.facenet = facenet
        self.facenet_embeddings = facenet_embeddings
        self.mobilenet = mobilenet
        self.mobilenet_embeddings = mobilenet_embeddings
        self.use_mobilenet = mobilenet is not None and mobilenet_embeddings is not None


    async def create_celebrity(self, name: str, image: Image.Image) -> None:

        prepared_photo = self.facenet.get_prepared_photo(image)
        celeb_id = await self.celeb_repository.put_name(name)
        save_photo(prepared_photo, id=celeb_id)
        cropped_image_tensor = self.facenet.crop_face(image)
        
        facenet_emb = self.facenet.get_embedding(cropped_image_tensor)
        self.facenet_embeddings.add_embedding(facenet_emb)

        if self.use_mobilenet:
            mobilenet_emb = self.mobilenet.get_embedding(cropped_image_tensor)
            self.mobilenet_embeddings.add_embedding(mobilenet_emb)
      