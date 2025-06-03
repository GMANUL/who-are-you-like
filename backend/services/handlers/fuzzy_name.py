from PIL import Image

from .base import AddCelebrityHandler
from .exceptions import ActionConfirmationRequired
from repositories.db.celeb_repository import CelebRepository


class FuzzyNameCheckHandler(AddCelebrityHandler):

    def __init__(self, celeb_repository: CelebRepository, next_handler=None):
        super().__init__(next_handler)
        self.celeb_repository = celeb_repository

    async def handle(self, name: str, image: Image.Image) -> None:

        similar_names = await self.celeb_repository.name_search(name, max_results=3, max_distance=5)
        if similar_names:
            raise ActionConfirmationRequired(
                message="Найдены похожие имена. Подтвердите добавление.",
                details={"similar_names": similar_names}
            )
        await super().handle(name, image)