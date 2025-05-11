from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel
import io
from services.face_service import FaceService
from services.photo_service import PhotoService


app = FastAPI(title="I like a celeb!")

face_service = FaceService()
photo_service = PhotoService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


class TopImages(BaseModel):
    matches: list

@app.post('/compare')
async def search_similar(
    file: UploadFile = File(..., description='Фото для сравнения')
):
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Пустой файл")
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        match_list = face_service.get_match_list(img)
        return TopImages(matches=match_list)
    
    except Image.UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат изображения")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Дебил, загрузи норм фотку")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка обработки: {str(e)}")


@app.get("/photo/{celeb_id}")
async def get_photo(celeb_id: int):
    return photo_service.get_celeb_photo(celeb_id)
