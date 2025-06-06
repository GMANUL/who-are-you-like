from torchvision.models import mobilenet_v3_small
from torchvision import transforms
from settings.settings import settings
import torch


class MobileNetV3Embedder(torch.nn.Module):

    def __init__(self, weights_path: str):
        super().__init__()
        self.base_model = mobilenet_v3_small(pretrained=False, weights=None)
        self.base_model.classifier = torch.nn.Identity()

        self._load_weights(weights_path)

        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])
    
    def _load_weights(self, weights_path):
        state_dict = torch.load(weights_path, map_location='cpu')
        
        state_dict = {k.replace('module.', ''): v for k, v in state_dict.items()}
        
        self.base_model.load_state_dict(state_dict, strict=False)


    def forward(self, x):
        x = self.preprocess(x)
        x = self.base_model(x)
        return x