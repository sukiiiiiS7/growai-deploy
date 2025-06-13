from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Dict
from io import BytesIO
from PIL import Image
import torch
import torchvision.transforms as transforms
import sys
import os
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.append(PROJECT_ROOT)

# Import score computation and environment bonus logic
from leaf.scoring.health_score import calculate_health_score
from leaf.scoring.env_bonus import calculate_environment_bonus

MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "leaf", "leaf_classifier_final_augmented.pth")
)
# Initialize FastAPI router
router = APIRouter(prefix="/leaf", tags=["Leaf Scan"])

from torchvision import models

# Initialize ResNet18 model (no pretrained weights)
model = models.resnet18(pretrained=False)

# Adjust the final layer for 2-class classification
model.fc = torch.nn.Linear(model.fc.in_features, 2)

# Load the state_dict (weights only)
state_dict = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
model.load_state_dict(state_dict)

# Set to evaluation mode
model.eval()


# Define image preprocessing pipeline (must match training)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Index-to-label mapping (based on training classes)
idx_to_label = {
    0: "healthy",
    1: "wilted"
}
def extract_leaf_features(img: Image.Image) -> dict:
    """
    Analyze leaf image and extract basic visual features.
    Returns features in the format required by calculate_leaf_score.
    """
    np_img = np.array(img)

    # Convert to HSV for better color segmentation
    hsv = np.array(img.convert("HSV"))

    # --- Color Features ---
    yellow_mask = ((hsv[:, :, 0] >= 20) & (hsv[:, :, 0] <= 40)) & (hsv[:, :, 1] > 50)
    brown_mask = ((hsv[:, :, 0] >= 10) & (hsv[:, :, 0] <= 20)) & (hsv[:, :, 1] > 30)

    yellow_ratio = yellow_mask.sum() / (np_img.shape[0] * np_img.shape[1])
    brown_pixels = brown_mask.sum()

    # --- Shape Features (dummy logic, improve later) ---
    irregularity = 0.3  # Fixed for now
    holes_detected = False  # Not implemented yet

    return {
        "color": {
            "yellow_ratio": round(float(yellow_ratio), 2),
            "brown": int(brown_pixels)
        },
        "shape": {
            "irregularity": irregularity,
            "holes_detected": holes_detected
        }
    }
@router.post("/scan", summary="Scan Leaf Health", description="Upload a leaf image and optional environment data to analyze plant health.")
async def scan_leaf(
    image: UploadFile = File(..., description="Leaf image (.jpg/.png)"),
    light_level: float = Form(50.0, description="Light level (0-100, optional)"),
    soil_moisture: float = Form(50.0, description="Soil moisture (0-100, optional)")
):
    """
    Main API endpoint: analyzes the uploaded leaf image and optional environment data,
    and returns a comprehensive health report.

    Parameters:
    - image: Leaf image file
    - light_level: Ambient light value (default 50)
    - soil_moisture: Soil moisture level (default 50)

    Returns:
    - health_score: Final health score (0–100)
    - label: Predicted category by the model (Healthy / Mild Wilt / Health Warning)
    - components: Sub-scores like image_score and env_bonus
    - explanation: Comments on environmental factors
    - recommendations: Care suggestions for the plant

    - explanation: Comments on environmental factors (e.g., "Light level is optimal.")
    - recommendations: Adaptive suggestions based on detected issues (e.g., "Watering is recommended.")
    - components.image_score: Derived from visual cues (color, shape, black spots)
    - components.env_bonus: Scored from light & soil inputs (range: -10 to +10)
    """
    try:
        # 1. Read and open image
        contents = await image.read()
        img = Image.open(BytesIO(contents)).convert("RGB")

        # 2. Preprocess and predict with model
        input_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.nn.functional.softmax(output[0], dim=0)
            confidence, pred_idx = torch.max(probs, dim=0)
            label = idx_to_label[int(pred_idx)]

        # 3. Score environment based on inputs
        env_bonus, env_comments = calculate_environment_bonus(soil_moisture, light_level)

        # 4. Compute final health score and suggestions
        leaf_features = extract_leaf_features(img)

        result = calculate_health_score(
            leaf_features=leaf_features,
            soil_moisture=soil_moisture,
            light_level=light_level
        )

        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
