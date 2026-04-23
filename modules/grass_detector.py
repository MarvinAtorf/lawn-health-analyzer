import torch
import torch.nn as nn
import numpy as np
import cv2
from PIL import Image
import torchvision.transforms as transforms


class GrassDetectorCNN(nn.Module):
    def __init__(self):
        super(GrassDetectorCNN, self).__init__()

        self.enc1 = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 16, 3, padding=1),
            nn.ReLU()
        )
        self.pool1 = nn.MaxPool2d(2)

        self.enc2 = nn.Sequential(
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.ReLU()
        )
        self.pool2 = nn.MaxPool2d(2)

        self.up1 = nn.ConvTranspose2d(32, 16, 2, stride=2)
        self.dec1 = nn.Sequential(
            nn.Conv2d(32, 16, 3, padding=1),
            nn.ReLU()
        )

        self.up2 = nn.ConvTranspose2d(16, 8, 2, stride=2)
        self.dec2 = nn.Sequential(
            nn.Conv2d(24, 8, 3, padding=1),
            nn.ReLU()
        )

        self.output = nn.Conv2d(8, 1, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool1(e1))
        d1 = self.dec1(torch.cat([self.up1(e2), e1], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d1),
                                  nn.functional.interpolate(e1, size=self.up2(d1).shape[2:])], dim=1))
        out = self.sigmoid(self.output(d2))
        return nn.functional.interpolate(out, size=(256, 256))

class GrassDetector:
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = GrassDetectorCNN().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])

    def predict(self, frame: np.ndarray) -> np.ndarray:
        """
        Nimmt einen BGR Frame (OpenCV) und gibt eine binäre Gras-Maske zurück.

        Returns:
            Binary mask (H, W) - 1 = Gras, 0 = kein Gras
        """
        # BGR → RGB → PIL
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        # Transform
        tensor = self.transform(pil_img).unsqueeze(0).to(self.device)

        # Prediction
        with torch.no_grad():
            output = self.model(tensor)

        # Binary mask
        mask = (output.squeeze().cpu().numpy() > 0.5).astype(np.uint8)

        # Resize zurück zur originalen Frame-Größe
        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]),
                          interpolation=cv2.INTER_NEAREST)

        return mask