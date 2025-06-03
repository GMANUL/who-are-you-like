from PIL import Image

from .base import AddCelebrityHandler
from .exceptions import NameAlreadyExistsError
from repositories.db.celeb_repository import CelebRepository


class ExactNameCheckHandler(AddCelebrityHandler):

    def __init__(self, celeb_repository: CelebRepository, next_handler=None):
        super().__init__(next_handler)
        self.celeb_repository = celeb_repository


    async def handle(self, name: str, image: Image.Image) -> None:

        if await self.celeb_repository.name_exists(name):
            raise NameAlreadyExistsError(f"Точное совпадение: '{name}' уже есть в базе.")
        await super().handle(name, image)
