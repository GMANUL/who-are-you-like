import os
from fastapi.responses import FileResponse
from settings.settings import settings


def get_photo(celeb_id: int) -> FileResponse:
    
    photo_path = os.path.join(settings.paths.images_dir, str(celeb_id), "1.jpg")
    return FileResponse(path=photo_path)
