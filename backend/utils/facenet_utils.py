import numpy as np
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image

class FaceNet:
    def __init__(self):
        self.embedding_model = InceptionResnetV1(pretrained='vggface2', classify=False).eval()
        self.crop_model = MTCNN(image_size=160, margin=20)

    def crop_face(self, image: Image.Image) -> torch.tensor:
        cropped_image = self.crop_model(image)
        if cropped_image is None:
            raise ValueError("Дебил, загрузи норм фотку")
        return cropped_image

    def get_embedding(self, image: Image.Image) -> np.ndarray:
        cropped_image_tensor = self.crop_face(image)
        with torch.no_grad():
            image_embedding = self.embedding_model(cropped_image_tensor.unsqueeze(0))

        return np.array(image_embedding).astype('float32')
