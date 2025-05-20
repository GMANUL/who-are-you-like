import os
from fastapi.responses import FileResponse

def get_photo(dir_path: str, celeb_id: int) -> FileResponse:
    photo_path = os.path.join("/app", dir_path, str(celeb_id), "1.jpg")
    print(photo_path)
    return FileResponse(path=photo_path)
