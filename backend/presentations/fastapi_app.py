from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel
import io
from typing import List, Union

from services.face_service import FaceService
from services.photo_service import PhotoService
from services.person_service import PersonService, ActionConfirmationRequired



app = FastAPI(title="I like a celeb!")

face_service = FaceService()
photo_service = PhotoService()
person_service = PersonService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


class MatchItem(BaseModel):
    id: int
    name: str
    distance: float

class MatchResponse(BaseModel):
    matches: List[MatchItem]

class NameResponse(BaseModel):
    names: List[str]

class ConfirmationResponse(BaseModel):
    status: str = "confirmation_required"
    message: str
    similar_names: list[str]
    


@app.post('/compare')
async def search_similar(file: UploadFile = File(..., description='Фото для сравнения')) -> MatchResponse:

    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Пустой файл")
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        match_list = await face_service.get_match_list(img)
        return MatchResponse(matches=match_list)
    
    except Image.UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат изображения")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка обработки: {str(e)}")


@app.get("/photo/{celeb_id}")
async def get_photo(celeb_id: int) -> FileResponse:

    return photo_service.get_celeb_photo(celeb_id)


@app.get("/search/{name_query}")
async def get_similar_names(name_query: str) -> NameResponse:

    name_list = await person_service.get_similar_names(name_query)
    return NameResponse(names=name_list)


@app.post("/new_celebrity")
async def create_celebrity(celeb_name: str = Form(..., min_length=3, max_length=25), 
                           file: UploadFile = File(..., description='Фото для новой знаменитости'),
                           force: bool = Form(False, description="Подтверждение добавления при наличии похожих имен")
                           ) -> Union[None, ConfirmationResponse]:
    
    try:
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Пустой файл")
        photo = Image.open(io.BytesIO(contents)).convert("RGB")
    
        await person_service.add_celebrity(celeb_name, photo, force=force)
    
    except ActionConfirmationRequired as e:
        return ConfirmationResponse(message=e.message, similar_names=e.details["similar_names"])

    except Image.UnidentifiedImageError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неподдерживаемый формат изображения")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка обработки: {str(e)}")