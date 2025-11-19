#!/bin/bash

# 台灣鳥類辨識器 - 完整工作流程腳本

echo "=================================="
echo "台灣鳥類辨識器 - 完整工作流程"
echo "=================================="
echo ""

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 步驟 1: 建立虛擬環境
echo -e "${YELLOW}步驟 1: 建立虛擬環境${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ 虛擬環境建立完成${NC}"
else
    echo -e "${GREEN}✓ 虛擬環境已存在${NC}"
fi
echo ""

# 步驟 2: 啟動虛擬環境
echo -e "${YELLOW}步驟 2: 啟動虛擬環境${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ 虛擬環境已啟動${NC}"
echo ""

# 步驟 3: 安裝依賴
echo -e "${YELLOW}步驟 3: 安裝依賴套件${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ 依賴套件安裝完成${NC}"
echo ""

# 步驟 4: 準備資料
echo -e "${YELLOW}步驟 4: 準備訓練資料${NC}"
cd src
python prepare_data.py
cd ..
echo ""

# 步驟 5: 提示使用者準備圖片
echo -e "${RED}⚠️  請注意: 需要手動準備圖片資料${NC}"
echo "請將鳥類照片放入以下資料夾："
echo "  - data/train/白尾八哥/"
echo "  - data/train/家八哥/"
echo "  - data/train/林八哥/"
echo "  - data/test/ (相同結構)"
echo ""
echo "按 Enter 鍵繼續（確認資料已準備完成）..."
read -r

# 步驟 6: 訓練模型
echo -e "${YELLOW}步驟 6: 訓練模型${NC}"
echo "選擇訓練方式："
echo "  1) 使用 Jupyter Notebook (推薦)"
echo "  2) 使用 Python 腳本"
echo -n "請選擇 [1/2]: "
read -r choice

if [ "$choice" = "1" ]; then
    echo -e "${GREEN}啟動 Jupyter Notebook...${NC}"
    jupyter notebook notebooks/bird_classifier_training.ipynb
elif [ "$choice" = "2" ]; then
    echo -e "${GREEN}開始訓練...${NC}"
    cd src
    python train.py
    cd ..
else
    echo -e "${RED}無效的選擇${NC}"
    exit 1
fi
echo ""

# 步驟 7: 測試模型
echo -e "${YELLOW}步驟 7: 啟動 Streamlit 應用${NC}"
echo "模型訓練完成後，按 Enter 啟動網頁應用..."
read -r

cd src
streamlit run app.py
