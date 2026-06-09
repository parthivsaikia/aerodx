import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
import shutil
from sklearn.model_selection import train_test_split

# =====================================================
# CHANGE THESE TWO PATHS ONLY
# =====================================================

COVID_PATH = r"C:\Users\User\Downloads\CT_COVID\CT_COVID"

NON_COVID_PATH = r"C:\Users\User\Downloads\CT_NonCOVID\CT_NonCOVID"

# Example:
# COVID_PATH = r"D:\Datasets\COVID_CT\covid"
# NON_COVID_PATH = r"D:\Datasets\COVID_CT\non_covid"

# =====================================================
# OUTPUT FOLDER
# =====================================================

OUTPUT_DIR = "dataset"

TRAIN_SIZE = 0.80
VALID_SIZE = 0.10
TEST_SIZE = 0.10

RANDOM_SEED = 42


def create_directory(path):
    os.makedirs(path, exist_ok=True)


def get_images(folder):

    valid_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff"
    )

    files = []

    for file in os.listdir(folder):

        full_path = os.path.join(folder, file)

        if os.path.isfile(full_path):

            if file.lower().endswith(valid_extensions):
                files.append(file)

    return files


def split_and_copy(source_folder, class_name):

    images = get_images(source_folder)

    print(f"\nFound {len(images)} images in {class_name}")

    train_files, temp_files = train_test_split(
        images,
        test_size=0.20,
        random_state=RANDOM_SEED,
        shuffle=True
    )

    valid_files, test_files = train_test_split(
        temp_files,
        test_size=0.50,
        random_state=RANDOM_SEED,
        shuffle=True
    )

    print(f"Train : {len(train_files)}")
    print(f"Valid : {len(valid_files)}")
    print(f"Test  : {len(test_files)}")

    split_map = {
        "train": train_files,
        "valid": valid_files,
        "test": test_files
    }

    for split_name, file_list in split_map.items():

        destination_folder = os.path.join(
            OUTPUT_DIR,
            split_name,
            class_name
        )

        create_directory(destination_folder)

        for file_name in file_list:

            src = os.path.join(
                source_folder,
                file_name
            )

            dst = os.path.join(
                destination_folder,
                file_name
            )

            shutil.copy2(src, dst)


def main():

    print("=" * 50)
    print("Preparing Dataset")
    print("=" * 50)

    if not os.path.exists(COVID_PATH):
        print("COVID folder not found!")
        return

    if not os.path.exists(NON_COVID_PATH):
        print("NON_COVID folder not found!")
        return

    split_and_copy(
        COVID_PATH,
        "covid"
    )

    split_and_copy(
        NON_COVID_PATH,
        "non_covid"
    )

    print("\nDataset preparation completed!")
    print("\nGenerated structure:\n")

    print(
        """
dataset/
│
├── train/
│   ├── covid/
│   └── non_covid/
│
├── valid/
│   ├── covid/
│   └── non_covid/
│
└── test/
    ├── covid/
    └── non_covid/
"""
    )


if __name__ == "__main__":
    main()


