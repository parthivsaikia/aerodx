# COVID-19 CT Scan Detector

A Deep Learning binary classification pipeline built in PyTorch using an EfficientNet backbone to detect COVID-19 presence from CT lung images.

## 📌 Project Overview
This repository provides a complete pipeline to train an image classification model and run individual inference tasks. It is designed to work efficiently even on constrained hardware environments by utilizing memory-optimized PyTorch data loading pipelines.

---

## 📂 Project Structure
```text
covid_detector_package/
│
├── dataset/
│   ├── train/
│   │   ├── covid/
│   │   └── non_covid/
│   └── valid/
│       ├── covid/
│       └── non_covid/
│
├── models/
│   └── covid_model.pth          # Saved best model weights
│
├── covid_model.py               # EfficientNet network architecture
├── train.py                     # Training & validation loop script
├── predict.py                   # Single image inference script
└── README.md                    # Project documentation


🛠️ Installation & Setup
1. Environment Activation
Open your PowerShell or Command Prompt terminal and activate your virtual environment:

Bash
.\venv312\Scripts\activate
2. Verify Core Dependencies
Ensure your environment contains the required version configurations for CUDA-accelerated deep learning:

Python: 3.12+

PyTorch: 2.5.1+cu121 (or newer compatible CUDA version)

Torchvision: 0.20.1+cu121

Pillow: 10.0.0+

🚀 How to Run
1. Training the Model
To start training the neural network on your dataset, configure your desired batch size and epochs in train.py, then execute:

Bash
python train.py
The script automatically selects your CUDA GPU if available. The best-performing model based on validation dataset accuracy will be saved to models/covid_model.pth.

2. Running Inference (Predictions)
To test a single CT scan image, update the IMAGE_PATH variable inside predict.py with the path to your image file, then run:

Bash
python predict.py
🔧 Troubleshooting & Known Fixes
1. Windows Page File / Out of Memory Crashes
If you encounter OSError: [WinError 1455] The paging file is too small or repetitive fatal: Memory allocation failure cycles when importing torch or starting an epoch:

Root Cause: PyTorch's large CUDA binaries (cufft64_11.dll) and dataset workers are exhausting physical RAM and virtual drive memory allocation limits.

Fix: 1. Open Windows Advanced System Settings -> Performance Settings -> Advanced tab.
2. Under Virtual Memory, select Change... and uncheck automatic management.
3. Select your system drive, click Custom Size, set Initial to 16000 MB and Maximum to 32000 MB.
4. Click Set, click OK, and restart your PC.

2. Data Loader Deadlocks or Crashing
To prevent subprocess multi-threading loops from overloading memory arrays on Windows platforms, ensure your DataLoader components in train.py use a single master thread execution pattern:

Python
num_workers=0
3. Model Image Standardization
To ensure correct feature matching from pre-trained ImageNet structures, both tracking loops (train.py) and single inference queries (predict.py) use synchronized scaling normalizations:

Python
transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)