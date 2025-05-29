from utils.photo_path import get_photo
from fastapi.responses import FileResponse


class PhotoService:
    def __init__(self) -> None:
        pass

    def get_celeb_photo(self, celeb_id: int) -> FileResponse:
        return get_photo(celeb_id)
