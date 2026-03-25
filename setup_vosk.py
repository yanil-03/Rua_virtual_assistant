import os
import zipfile
import requests
from tqdm import tqdm

# ---------------- CONFIG ----------------
MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip"
MODEL_ZIP = "vosk_model.zip"
TARGET_DIR = "models"
FINAL_DIR = os.path.join(TARGET_DIR, "vosk")

# ---------------- DOWNLOAD ----------------
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(filename, "wb") as file, tqdm(
        desc="Downloading Vosk Model",
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            bar.update(len(data))

# ---------------- EXTRACT ----------------
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

# ---------------- MAIN ----------------
def setup_vosk():
    print("🚀 Setting up Vosk model...")

    os.makedirs(TARGET_DIR, exist_ok=True)

    # Step 1: Download
    if not os.path.exists(MODEL_ZIP):
        download_file(MODEL_URL, MODEL_ZIP)
    else:
        print("📦 Model zip already exists, skipping download")

    # Step 2: Extract
    print("📂 Extracting...")
    extract_zip(MODEL_ZIP, TARGET_DIR)

    # Step 3: Rename folder
    extracted_folder = None
    for folder in os.listdir(TARGET_DIR):
        if "vosk-model" in folder:
            extracted_folder = os.path.join(TARGET_DIR, folder)
            break

    if extracted_folder is None:
        print("❌ Could not find extracted model folder")
        return

    # Remove old vosk folder if exists
    if os.path.exists(FINAL_DIR):
        print("⚠️ Removing old model...")
        import shutil
        shutil.rmtree(FINAL_DIR)

    os.rename(extracted_folder, FINAL_DIR)

    # Step 4: Cleanup zip
    os.remove(MODEL_ZIP)

    print("✅ Vosk model setup complete!")
    print(f"📍 Location: {FINAL_DIR}")

# ---------------- RUN ----------------
if __name__ == "__main__":
    setup_vosk()