import os
import requests
import zipfile
import shutil
from pathlib import Path
import random

# Dataset URL
DATASET_URL = 'https://github.com/yenlung/AI-Demo/raw/master/myna.zip'
ZIP_PATH = 'data/myna.zip'
EXTRACT_DIR = 'data/temp_extract'

# Mapping: Original Name -> Project Name
CATEGORY_MAPPING = {
    'javan_myna': '白尾八哥',
    'common_myna': '家八哥',
    'crested_myna': '林八哥'
}

def download_file(url, save_path):
    print(f"Downloading {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  ✓ Downloaded to {save_path}")
        return True
    except Exception as e:
        print(f"  ✗ Download failed: {e}")
        return False

def organize_data():
    base_dir = Path('data')
    train_dir = base_dir / 'train'
    test_dir = base_dir / 'test'
    temp_dir = Path(EXTRACT_DIR)

    # Clean up existing data
    if train_dir.exists(): shutil.rmtree(train_dir)
    if test_dir.exists(): shutil.rmtree(test_dir)
    
    train_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    print("Organizing data...")
    
    for original_name, target_name in CATEGORY_MAPPING.items():
        src_folder = temp_dir / original_name
        if not src_folder.exists():
            print(f"  ⚠️  Source folder not found: {src_folder}")
            continue
            
        print(f"  Processing {target_name} (from {original_name})...")
        
        # Get all images
        images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)
        
        # Split 80/20
        split_idx = int(len(images) * 0.8)
        train_images = images[:split_idx]
        test_images = images[split_idx:]
        
        # Create target directories
        (train_dir / target_name).mkdir(parents=True, exist_ok=True)
        (test_dir / target_name).mkdir(parents=True, exist_ok=True)
        
        # Copy files
        for img in train_images:
            shutil.copy(src_folder / img, train_dir / target_name / img)
            
        for img in test_images:
            shutil.copy(src_folder / img, test_dir / target_name / img)
            
        print(f"    Train: {len(train_images)}, Test: {len(test_images)}")

def main():
    # 1. Download
    if not download_file(DATASET_URL, ZIP_PATH):
        return

    # 2. Extract
    print("Extracting zip file...")
    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    print("  ✓ Extracted")

    # 3. Organize
    organize_data()

    # 4. Cleanup
    print("Cleaning up temporary files...")
    if os.path.exists(ZIP_PATH): os.remove(ZIP_PATH)
    if os.path.exists(EXTRACT_DIR): shutil.rmtree(EXTRACT_DIR)
    
    print("\nReal data preparation complete!")

if __name__ == "__main__":
    main()
