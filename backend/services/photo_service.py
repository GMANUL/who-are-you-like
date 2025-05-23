from utils.photo_path import get_photo
from fastapi.responses import FileResponse


class PhotoService:
    def __init__(self, image_dir:str = "C:\\face_dataset\\faces_imdb_test"):
        self.image_dir = image_dir

    def get_celeb_photo(self, celeb_id: int) -> FileResponse:
        return get_photo(self.image_dir, celeb_id)
