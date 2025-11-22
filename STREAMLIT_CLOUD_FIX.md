# Streamlit Cloud 部署修復指南

## 問題診斷

從錯誤日誌發現以下問題：

1. **TensorFlow 版本不相容**：`tensorflow==2.16.2` 不支援 Python 3.13
2. **Mac 專用套件**：`tensorflow-metal==1.2.0` 只能在 macOS 上運行，Streamlit Cloud 使用 Linux

## 已修復的問題

### 1. 更新 `requirements.txt`

**修改前：**
```text
streamlit>=1.30.0
tensorflow==2.16.2
tensorflow-metal==1.2.0  # ❌ Mac 專用
pillow>=10.0.0
numpy<2.0.0
matplotlib>=3.8.0
pandas>=2.1.0
setuptools<70
```

**修改後：**
```text
streamlit>=1.30.0
tensorflow>=2.20.0  # ✅ 支援 Python 3.10-3.13
pillow>=10.0.0
numpy>=1.23.0,<2.0.0
matplotlib>=3.8.0
pandas>=2.1.0
```

### 2. 指定 Python 版本

建立 `.python-version` 檔案，內容為：
```
3.11
```

這會告訴 Streamlit Cloud 使用 Python 3.11（也可以選擇 3.10、3.12 或 3.13）。

### 3. 移除不必要的 imports

從 `src/app.py` 移除：
```python
# Fix for Python 3.12 distutils issue
import setuptools
import distutils
```

這些是為了解決本地 Mac 問題而加入的，Streamlit Cloud 不需要。

## 部署步驟

### 方法 1：推送到 GitHub（推薦）

```bash
# 1. 提交修改
git add .
git commit -m "Fix: Update dependencies for Streamlit Cloud compatibility"

# 2. 推送到 GitHub
git push origin main
```

Streamlit Cloud 會自動偵測變更並重新部署。

### 方法 2：手動重新部署

1. 前往 [Streamlit Cloud Dashboard](https://share.streamlit.io/)
2. 找到你的應用程式
3. 點擊 "Reboot app" 或 "Redeploy"

## Python 版本選擇

TensorFlow 2.20.0 支援的 Python 版本：
- ✅ Python 3.10
- ✅ Python 3.11（推薦）
- ✅ Python 3.12
- ✅ Python 3.13

建議使用 **Python 3.11** 或 **3.12**，因為它們最穩定且廣泛使用。

## 驗證部署

部署成功後，你應該會看到：
1. ✅ Dependencies 安裝成功
2. ✅ App 正常啟動
3. ✅ 可以上傳圖片並進行辨識

## 常見問題

### Q: 本地環境怎麼辦？

如果你在 Mac 上開發，可以建立兩個 requirements 檔案：

**requirements.txt**（用於 Streamlit Cloud）：
```text
streamlit>=1.30.0
tensorflow>=2.20.0
pillow>=10.0.0
numpy>=1.23.0,<2.0.0
matplotlib>=3.8.0
pandas>=2.1.0
```

**requirements-mac.txt**（用於本地 Mac 開發）：
```text
streamlit>=1.30.0
tensorflow>=2.20.0
tensorflow-metal>=1.2.0
pillow>=10.0.0
numpy>=1.23.0,<2.0.0
matplotlib>=3.8.0
pandas>=2.1.0
```

本地安裝時使用：
```bash
pip install -r requirements-mac.txt
```

### Q: 如果還是失敗怎麼辦？

1. 檢查 Streamlit Cloud 的日誌
2. 確認 `.python-version` 檔案已提交
3. 確認 `requirements.txt` 沒有 Mac 專用套件
4. 嘗試清除快取後重新部署

## 參考資料

- [TensorFlow 版本相容性](https://www.tensorflow.org/install/pip)
- [Streamlit Cloud 文件](https://docs.streamlit.io/streamlit-community-cloud)
