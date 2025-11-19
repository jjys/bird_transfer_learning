# Streamlit Cloud 部署修正

## ❌ 原本的錯誤

```
ERROR: Could not find a version that satisfies the requirement tensorflow==2.15.0
```

**原因**: Streamlit Cloud 使用 Python 3.13，但 TensorFlow 2.15.0 不支援 Python 3.13。

## ✅ 解決方案

### 1. 更新 requirements.txt

```txt
# 舊版（不相容）
tensorflow==2.15.0
keras==2.15.0

# 新版（相容 Python 3.11-3.13）
tensorflow>=2.20.0
# keras 已整合在 TensorFlow 2.20+ 中
```

### 2. 指定 Python 版本

創建 `.python-version` 文件：
```
python = "3.11"
```

這會讓 Streamlit Cloud 使用 Python 3.11（最穩定的版本）。

### 3. 更新程式碼

`app.py` 中改用相容的 import：

```python
try:
    # TensorFlow 2.20+ 使用 keras 3
    import keras
except ImportError:
    # 舊版使用 tensorflow.keras
    from tensorflow import keras
```

## 🚀 重新部署步驟

### 方法 1: 更新現有部署

```bash
# 在 HW4 目錄下
git add .
git commit -m "Fix: Update dependencies for Streamlit Cloud compatibility"
git push
```

Streamlit Cloud 會自動檢測變更並重新部署。

### 方法 2: 從頭開始

如果還沒推送到 GitHub：

```bash
cd /Users/jys922/Documents/myproject/testProject/IoT/HW4

# 初始化（如果已做過可跳過）
git init
git branch -M main

# 添加所有檔案
git add .
git commit -m "Initial commit: Taiwan Bird Classifier with fixed dependencies"

# 連接到遠端 repo
git remote add origin https://github.com/你的用戶名/repo名稱.git
git push -u origin main
```

## 📋 檢查清單

部署前確認：

- [ ] `requirements.txt` 已更新為相容版本
- [ ] `.python-version` 檔案已創建
- [ ] `.streamlit/config.toml` 檔案已創建
- [ ] `app.py` 的 import 已更新
- [ ] 模型檔案大小 < 100MB 或已設定 Git LFS
- [ ] 所有變更已 commit 並 push

## 🐛 如果還是失敗

### 選項 A: 使用更穩定的版本

修改 `requirements.txt`：

```txt
streamlit==1.39.0
tensorflow==2.20.0
pillow==10.4.0
numpy==1.26.0
matplotlib==3.9.0
pandas==2.2.0
```

### 選項 B: 移除模型預載入

如果記憶體不足，修改 `app.py`：

```python
@st.cache_resource
def load_model():
    """延遲載入模型"""
    if 'model' not in st.session_state:
        model_path = '../models/bird_classifier.keras'
        if os.path.exists(model_path):
            st.session_state['model'] = keras.models.load_model(model_path)
    return st.session_state.get('model'), None
```

### 選項 C: 使用更輕量的模型

如果檔案太大，重新訓練時使用：
- MobileNetV3Small（更小）
- 更少的 Dense 層
- 量化模型（減少精度但縮小大小）

## 📊 版本相容性表

| Python | TensorFlow | Keras | Streamlit |
|--------|------------|-------|-----------|
| 3.9    | 2.15.0     | 2.15.0| 1.30+     |
| 3.10   | 2.15.0     | 2.15.0| 1.30+     |
| 3.11   | 2.20.0     | 3.x   | 1.30+     |
| 3.12   | 2.20.0     | 3.x   | 1.30+     |
| 3.13   | 2.20.0     | 3.x   | 1.30+     |

## 🎯 推薦配置（最穩定）

```txt
# requirements.txt
streamlit==1.39.0
tensorflow==2.20.0
pillow==10.4.0
numpy==1.26.4
matplotlib==3.9.2
pandas==2.2.3
```

```
# .python-version
python = "3.11"
```

## 💡 額外提示

1. **檢查部署日誌**: 在 Streamlit Cloud 控制台查看即時錯誤
2. **測試本地**: 先在本地測試新版本是否能運行
3. **分階段更新**: 一次更新一個套件，確認沒問題再繼續
4. **使用範圍版本**: `>=2.20.0` 比 `==2.20.0` 更靈活

## ✅ 確認部署成功

部署成功後應該看到：

```
✅ App is running
🎈 Your app is live at: https://你的app網址.streamlit.app
```

可以測試：
1. 上傳圖片
2. 查看預測結果
3. 確認所有功能正常

---

**更新時間**: 2025-11-19  
**狀態**: 已修正相容性問題
