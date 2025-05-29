import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from settings.settings import settings


class FaceNet:

    def __init__(self) -> None:

        self.embedding_model = InceptionResnetV1(pretrained=None, classify=False).eval()
        state_dict = torch.load(settings.paths.embedding_model)
        self.embedding_model.load_state_dict(state_dict, strict=False)

        self.crop_model = MTCNN(image_size=160, margin=20)


    def crop_face(self, image: Image.Image) -> torch.tensor:

        cropped_image = self.crop_model(image)
        if cropped_image is None:
            raise FaceDetectionError()
        return cropped_image


    def get_embedding(self, image: Image.Image) -> np.ndarray:

        cropped_image_tensor = self.crop_face(image)
        with torch.no_grad():
            image_embedding = self.embedding_model(cropped_image_tensor.unsqueeze(0))

        return np.array(image_embedding).astype('float32')
    

    def get_prepared_photo(self, image: Image.Image) -> Image.Image:

        image_tensor = self.crop_face(image)
        image_tensor = (image_tensor + 1) / 2 
        image_array = image_tensor.permute(1, 2, 0).mul(255).byte().numpy()
        pil_photo = Image.fromarray(image_array)
        resized_photo = pil_photo.resize((256, 256), Image.LANCZOS)
        return resized_photo



class FaceDetectionError(Exception):

    def __init__(self) -> None:
        super().__init__("Дебил, загрузи норм фотку")
    