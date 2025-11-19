# 部署到 Streamlit Cloud 指南

## 📋 前置準備

1. GitHub 帳號
2. Streamlit Cloud 帳號（使用 GitHub 登入）
3. 已訓練好的模型檔案

## 🔧 步驟 1: 準備 GitHub Repository

### 1.1 初始化 Git（如果尚未初始化）

```bash
cd /path/to/IoT/HW4
git init
git add .
git commit -m "Initial commit: Taiwan Bird Classifier"
```

### 1.2 創建 GitHub Repository

1. 前往 https://github.com/new
2. 填寫 repository 名稱，例如：`taiwan-bird-classifier`
3. 選擇 Public（Streamlit Cloud 免費版需要）
4. 不要初始化 README（因為已經有了）
5. 點擊 "Create repository"

### 1.3 推送到 GitHub

```bash
git remote add origin https://github.com/你的用戶名/taiwan-bird-classifier.git
git branch -M main
git push -u origin main
```

## ⚠️ 步驟 2: 處理模型檔案大小問題

GitHub 限制單一檔案大小為 100MB，模型檔案可能會超過。

### 方案 A: 使用 Git LFS（推薦）

```bash
# 安裝 Git LFS
brew install git-lfs  # macOS
# 或參考 https://git-lfs.github.com/ 其他平台安裝方式

# 初始化 LFS
git lfs install

# 追蹤模型檔案
git lfs track "models/*.keras"
git lfs track "models/*.h5"

# 添加 .gitattributes
git add .gitattributes

# 提交並推送
git add models/
git commit -m "Add model files with LFS"
git push
```

### 方案 B: 在應用啟動時下載模型

修改 `src/app.py`，在 `load_model()` 函數中加入下載邏輯：

```python
import gdown

@st.cache_resource
def load_model():
    model_path = '../models/bird_classifier.keras'
    
    # 如果模型不存在，從 Google Drive 下載
    if not os.path.exists(model_path):
        st.info("首次啟動，正在下載模型...")
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Google Drive 分享連結的 file ID
        file_id = "你的_Google_Drive_檔案ID"
        url = f"https://drive.google.com/uc?id={file_id}"
        
        gdown.download(url, model_path, quiet=False)
    
    model = keras.models.load_model(model_path)
    return model, None
```

並在 `requirements.txt` 加入 `gdown`。

## 🌐 步驟 3: 部署到 Streamlit Cloud

### 3.1 登入 Streamlit Cloud

1. 前往 https://streamlit.io/cloud
2. 點擊 "Sign up" 或 "Sign in"
3. 使用 GitHub 帳號登入

### 3.2 部署應用

1. 點擊 "New app"
2. 填寫部署資訊：
   - **Repository**: 選擇你的 `taiwan-bird-classifier`
   - **Branch**: `main`
   - **Main file path**: `src/app.py`
   - **App URL**: 選擇一個網址（可自訂或使用預設）

3. 點擊 "Advanced settings"（可選）：
   - **Python version**: 選擇 3.9 或 3.10
   - **Secrets**: 如果有 API key 等敏感資訊

4. 點擊 "Deploy!"

### 3.3 等待部署完成

- 首次部署約需 5-10 分鐘
- 可以看到即時的部署日誌
- 部署成功後會自動開啟應用

## 📝 步驟 4: 設定檔案路徑

Streamlit Cloud 的檔案結構可能與本地不同，修改 `src/app.py` 的路徑：

```python
# 修改前
model_path = '../models/bird_classifier.keras'

# 修改後（更彈性的路徑處理）
import os
from pathlib import Path

# 取得專案根目錄
project_root = Path(__file__).parent.parent
model_path = project_root / 'models' / 'bird_classifier.keras'
```

## ✅ 步驟 5: 驗證部署

1. 等待部署完成（看到綠色 "Running"）
2. 點擊應用 URL
3. 測試上傳圖片功能
4. 確認預測結果正確

## 🔄 更新應用

當你修改程式碼後：

```bash
git add .
git commit -m "Update: 描述你的修改"
git push
```

Streamlit Cloud 會自動檢測到變更並重新部署。

## 🐛 常見問題排查

### 問題 1: 模組找不到

**錯誤訊息**: `ModuleNotFoundError: No module named 'xxx'`

**解決方法**:
- 確認 `requirements.txt` 包含所有依賴
- 版本號要明確（如 `tensorflow==2.15.0`）

### 問題 2: 記憶體不足

**錯誤訊息**: `MemoryError` 或應用崩潰

**解決方法**:
- 使用更輕量的模型（如 MobileNetV2 而非 ResNet）
- 減少模型參數
- 考慮升級到 Streamlit Cloud 付費方案

### 問題 3: 模型載入失敗

**錯誤訊息**: 找不到模型檔案

**解決方法**:
- 確認模型檔案已正確上傳到 GitHub
- 使用方案 B（動態下載模型）
- 檢查檔案路徑是否正確

### 問題 4: 部署超時

**解決方法**:
- 檢查 `requirements.txt` 是否有不必要的大型套件
- 確認網路連線正常
- 重新嘗試部署

## 🎉 成功部署後

你的應用現在可以：
- 透過公開 URL 訪問
- 分享給任何人使用
- 自動更新（當你推送新程式碼時）

## 📊 監控和管理

在 Streamlit Cloud 控制台可以：
- 查看應用日誌
- 監控資源使用
- 重啟應用
- 刪除應用

## 💡 進階技巧

1. **自訂網域**: 升級到付費方案可以使用自己的網域
2. **私有應用**: 設定密碼保護
3. **環境變數**: 使用 Secrets 管理敏感資訊
4. **多個應用**: 可以部署多個不同的專案

## 🔗 相關資源

- [Streamlit Cloud 文件](https://docs.streamlit.io/streamlit-community-cloud)
- [Git LFS 文件](https://git-lfs.github.com/)
- [GitHub 使用指南](https://docs.github.com/)
