import torch

from PIL import Image
from torchvision import transforms

from covid_model import CovidModel

# ======================================================
# CONFIGURATION
# ======================================================

MODEL_PATH = "models/covid_model.pth"

# Change this to your CT image path
IMAGE_PATH = r"C:\Users\User\Downloads\CT_COVID\CT_COVID\2020.02.10.20021584-p6-52%11.png"

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print(f"\nUsing Device : {DEVICE}\n")

# ======================================================
# LOAD MODEL
# ======================================================

model = CovidModel()

# FIX 1: Added weights_only=True to resolve the security FutureWarning
model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True 
    )
)

model = model.to(DEVICE)
model.eval()

print("Model Loaded Successfully!")

# ======================================================
# IMAGE TRANSFORM
# ======================================================

# FIX 2: Added Image Net normalization statistics. 
# EfficientNet expects inputs to match the scale/distribution it was trained on.
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ======================================================
# LOAD IMAGE
# ======================================================

image = Image.open(
    IMAGE_PATH
).convert("RGB")

image_tensor = transform(image)
image_tensor = image_tensor.unsqueeze(0)
image_tensor = image_tensor.to(DEVICE)

# ======================================================
# PREDICTION
# ======================================================

with torch.no_grad():
    output = model(image_tensor)
    probability = torch.sigmoid(output)
    confidence = probability.item()

# ======================================================
# RESULT
# ======================================================

print("=" * 50)
print(f"COVID Probability : {confidence:.4f}")

if confidence >= 0.5:
    print("\nPrediction : COVID POSITIVE")
    print(f"Confidence : {confidence * 100:.2f}%")
else:
    print("\nPrediction : NON COVID")
    print(f"Confidence : {(1 - confidence) * 100:.2f}%")

print("=" * 50)