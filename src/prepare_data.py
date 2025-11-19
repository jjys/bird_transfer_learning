"""
資料準備腳本
下載並整理鳥類圖片資料
"""

import os
import requests
import zipfile
from pathlib import Path

def create_directory_structure():
    """建立資料夾結構"""
    directories = [
        '../data/train/白尾八哥',
        '../data/train/家八哥',
        '../data/train/林八哥',
        '../data/test/白尾八哥',
        '../data/test/家八哥',
        '../data/test/林八哥'
    ]
    
    print("建立資料夾結構...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    
    print("\n資料夾結構建立完成！")


def print_instructions():
    """印出手動準備資料的說明"""
    print("\n" + "=" * 70)
    print("資料準備說明")
    print("=" * 70)
    print()
    print("請手動準備鳥類圖片，並放置到以下資料夾：")
    print()
    print("訓練資料（每個資料夾至少 50 張圖片）：")
    print("  📁 data/train/白尾八哥/")
    print("  📁 data/train/家八哥/")
    print("  📁 data/train/林八哥/")
    print()
    print("測試資料（每個資料夾至少 10 張圖片）：")
    print("  📁 data/test/白尾八哥/")
    print("  📁 data/test/家八哥/")
    print("  📁 data/test/林八哥/")
    print()
    print("=" * 70)
    print("資料來源建議")
    print("=" * 70)
    print()
    print("1. Google 圖片搜尋")
    print("   - 搜尋「白尾八哥」、「家八哥」、「林八哥」")
    print("   - 選擇清晰、完整的鳥類照片")
    print("   - 避免使用有版權問題的圖片")
    print()
    print("2. iNaturalist (https://www.inaturalist.org/)")
    print("   - 開放授權的生物觀察照片")
    print("   - 搜尋對應的英文名稱")
    print()
    print("3. Flickr Creative Commons")
    print("   - 搜尋開放授權的鳥類照片")
    print()
    print("4. 自行拍攝")
    print("   - 最推薦的方式")
    print("   - 可以確保資料品質和版權")
    print()
    print("=" * 70)
    print("圖片要求")
    print("=" * 70)
    print()
    print("✓ 格式：JPG, JPEG, PNG")
    print("✓ 大小：至少 224x224 像素（會自動調整）")
    print("✓ 內容：鳥類主體清晰可見")
    print("✓ 光線：充足且均勻")
    print("✓ 角度：多樣化（正面、側面、飛行等）")
    print()
    print("建議每個類別準備：")
    print("  • 訓練集：50-100 張")
    print("  • 測試集：10-20 張")
    print()
    print("=" * 70)
    print()
    print("完成資料準備後，執行以下指令開始訓練：")
    print("  python train.py")
    print()


def check_data_ready():
    """檢查資料是否已準備好"""
    print("\n檢查資料準備狀況...")
    print()
    
    classes = ['白尾八哥', '家八哥', '林八哥']
    ready = True
    
    for class_name in classes:
        train_path = f'../data/train/{class_name}'
        test_path = f'../data/test/{class_name}'
        
        train_count = len([f for f in os.listdir(train_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]) if os.path.exists(train_path) else 0
        test_count = len([f for f in os.listdir(test_path) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg'))]) if os.path.exists(test_path) else 0
        
        print(f"{class_name}:")
        print(f"  訓練集: {train_count} 張")
        print(f"  測試集: {test_count} 張")
        
        if train_count < 20:
            print(f"  ⚠️  警告: 訓練資料不足（建議至少 50 張）")
            ready = False
        elif train_count < 50:
            print(f"  ⚠️  建議: 增加更多訓練資料以提升效果")
        else:
            print(f"  ✓ 訓練資料充足")
        
        print()
    
    if ready:
        print("✓ 資料準備完成！可以開始訓練模型。")
    else:
        print("⚠️  部分類別資料不足，建議補充更多圖片。")
    
    return ready


def create_sample_readme():
    """建立資料夾的 README"""
    readme_content = """# 鳥類圖片資料

## 資料夾說明

- `train/`: 訓練資料
- `test/`: 測試資料

## 類別

1. 白尾八哥 (Javan Myna)
2. 家八哥 (Common Myna)
3. 林八哥 (Great Myna)

## 資料準備步驟

1. 蒐集各類別的鳥類照片
2. 將照片放入對應的資料夾
3. 確保圖片清晰且主體明確
4. 建議每個類別至少 50 張訓練圖片

## 資料來源

- 請確保使用的圖片有適當的授權
- 建議來源：
  - Google 圖片搜尋（注意版權）
  - iNaturalist
  - Flickr Creative Commons
  - 自行拍攝

## 注意事項

- 圖片格式：JPG, JPEG, PNG
- 圖片大小：會自動調整為 224x224
- 避免使用有浮水印的圖片
- 確保圖片品質良好
"""
    
    readme_path = '../data/README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n資料夾說明文件已建立: {readme_path}")


def main():
    print("\n" + "=" * 70)
    print("台灣鳥類辨識器 - 資料準備工具")
    print("=" * 70)
    print()
    
    # 建立資料夾結構
    create_directory_structure()
    
    # 建立 README
    create_sample_readme()
    
    # 顯示說明
    print_instructions()
    
    # 檢查資料狀況
    check_data_ready()
    
    print("\n" + "=" * 70)
    print("資料準備工具執行完成")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
