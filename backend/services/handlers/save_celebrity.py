from PIL import Image

from .base import AddCelebrityHandler
from services.factories.celebrity_factory import CelebrityFactory


class SaveCelebrityHandler(AddCelebrityHandler):

    def __init__(self, factory: CelebrityFactory):
        super().__init__()
        self.factory = factory


    async def handle(self, name: str, image: Image.Image) -> None:
        await self.factory.create_celebrity(name, image)