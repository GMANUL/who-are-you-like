from abc import ABC, abstractmethod
from typing import Optional
from PIL import Image


class AddCelebrityHandler(ABC):
    
    def __init__(self, next_handler: Optional["AddCelebrityHandler"] = None):
        self.next_handler = next_handler

    @abstractmethod
    async def handle(self, name: str, image: Image.Image) -> None:
        if self.next_handler:
            await self.next_handler.handle(name, image)