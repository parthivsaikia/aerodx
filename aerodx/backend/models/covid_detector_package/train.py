import os
# These help restrict CPU-bound multi-threading overhead
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import copy
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

from covid_model import CovidModel

# ======================================================
# CONFIGURATION
# ======================================================

# FIX 1: Reduced batch size from 16 to 8 to prevent GPU Out Of Memory errors
BATCH_SIZE = 8 
EPOCHS = 15
LEARNING_RATE = 0.0001
IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available()
    else "cpu"
)

print(f"\nUsing Device : {DEVICE}\n")

# ======================================================
# DATA TRANSFORMS
# ======================================================

train_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.RandomAffine(
        degrees=0,
        translate=(0.05, 0.05)
    ),
    transforms.ColorJitter(
        brightness=0.1,
        contrast=0.1
    ),
    transforms.ToTensor()
])

valid_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])

# ======================================================
# LOAD DATASET
# ======================================================

train_dataset = ImageFolder(
    root="dataset/train",
    transform=train_transform
)

valid_dataset = ImageFolder(
    root="dataset/valid",
    transform=valid_transform
)

# FIX 2: Added num_workers=0 to eliminate the "fatal : Memory allocation failure" on Windows
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print("Classes Found :", train_dataset.classes)
print("Training Images :", len(train_dataset))
print("Validation Images :", len(valid_dataset))

# ======================================================
# LOAD MODEL
# ======================================================

model = CovidModel()
model = model.to(DEVICE)

# ======================================================
# LOSS FUNCTION
# ======================================================

criterion = nn.BCEWithLogitsLoss()

# ======================================================
# OPTIMIZER
# ======================================================

optimizer = optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=1e-4
)

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)

# ======================================================
# TRAINING
# ======================================================

best_accuracy = 0.0
best_model = copy.deepcopy(model.state_dict())

os.makedirs("models", exist_ok=True)

for epoch in range(EPOCHS):

    print("=" * 60)
    print(f"Epoch {epoch+1}/{EPOCHS}")
    print("=" * 60)

    # ---------------- TRAIN ----------------

    model.train()
    running_loss = 0.0

    for images, labels in train_loader:

        images = images.to(DEVICE)
        labels = labels.float().unsqueeze(1)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    train_loss = running_loss / len(train_loader)

    # ---------------- VALIDATION ----------------

    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in valid_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(images)
            probabilities = torch.sigmoid(outputs)
            predictions = (probabilities > 0.5).float()

            # FIX 3: Added flattening to match dimensions safely during multi-batch accuracy tracking
            correct += (predictions.view(-1) == labels.view(-1)).sum().item()
            total += labels.size(0)

    validation_accuracy = correct / total
    scheduler.step(validation_accuracy)

    print(f"Train Loss : {train_loss:.4f}")
    print(f"Validation Accuracy : {validation_accuracy*100:.2f}%")

    # ---------------- SAVE BEST MODEL ----------------

    if validation_accuracy > best_accuracy:
        best_accuracy = validation_accuracy
        best_model = copy.deepcopy(model.state_dict())
        torch.save(best_model, "models/covid_model.pth")
        print("Best model saved!")

print("\n")
print("=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

print(f"Best Validation Accuracy : {best_accuracy*100:.2f}%")
print("\nModel Saved At : models/covid_model.pth")