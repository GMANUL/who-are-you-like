from PIL import Image
from typing import List

from repositories.db.celeb_repository import CelebRepository
from utils.embedding_utils import Embeddings
from utils.facenet_utils import FaceNet
from utils.save_photo_utils import save_photo

class PersonService:

    def __init__(self) -> None:
        self.celeb_repository = CelebRepository()
        self.embeddings = Embeddings()
        self.facenet = FaceNet()
    

    async def get_similar_names(self, query: str) -> List[str]:
        
        return await self.celeb_repository.name_search(query)
    
    
    async def add_celebrity(self, name: str, image: Image.Image) -> None:
        
        if await self.celeb_repository.name_exists(name):
            raise NameAlreadyExistsError(name)
        
        celeb_embedding = self.facenet.get_embedding(image)
        prepared_photo = self.facenet.get_prepared_photo(image)

        celeb_id = await self.celeb_repository.put_name(name)
        save_photo(prepared_photo, id=celeb_id)

        self.embeddings.add_embedding(celeb_embedding)


class NameAlreadyExistsError(Exception):
    
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Имя '{name}' уже существует")
