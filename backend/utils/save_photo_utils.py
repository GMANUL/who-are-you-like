import os
from PIL import Image
from settings.settings import settings


def save_photo(image: Image.Image, id: int) -> None:
    
    photo_dir = os.path.join(settings.paths.images_dir, str(id))
    os.makedirs(photo_dir, exist_ok=True)
    photo_path = os.path.join(photo_dir, "1.jpg")
    image.save(photo_path)