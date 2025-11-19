# 快速開始指南

## 🚀 三步驟開始使用

### 步驟 1: 安裝依賴

```bash
# 建立虛擬環境（建議）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 安裝套件
pip install -r requirements.txt
```

### 步驟 2: 準備資料

```bash
# 執行資料準備腳本
cd src
python prepare_data.py
```

然後依照指示手動放置鳥類圖片到 `data/train/` 和 `data/test/` 資料夾。

### 步驟 3A: 使用 Notebook 訓練（推薦）

```bash
jupyter notebook notebooks/bird_classifier_training.ipynb
```

### 步驟 3B: 或使用腳本訓練

```bash
cd src
python train.py
```

### 步驟 4: 啟動網頁應用

```bash
cd src
streamlit run app.py
```

## 📊 預期結果

- 訓練時間: 10-20 分鐘（依硬體而定）
- 訓練準確率: ~90%
- 驗證準確率: ~85%

## 🐛 常見問題

### Q: pip install 失敗？

```bash
# 升級 pip
pip install --upgrade pip

# 分別安裝
pip install tensorflow
pip install streamlit
pip install pillow numpy matplotlib pandas
```

### Q: TensorFlow 安裝問題（Apple Silicon Mac）？

```bash
# 使用 metal 加速版本
pip install tensorflow-metal
```

### Q: 沒有 GPU 訓練很慢？

使用 Google Colab 免費 GPU：
1. 上傳 notebook 到 Colab
2. 修改資料路徑到 Google Drive
3. 啟用 GPU 加速

## 📝 下一步

- 增加更多訓練資料
- 調整超參數
- 嘗試其他預訓練模型
- 部署到 Streamlit Cloud
