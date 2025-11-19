"""
台灣鳥類辨識器 - Streamlit 網頁應用
使用遷移式學習識別台灣常見八哥科鳥類
"""

import streamlit as st
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
import os
import requests
from io import BytesIO

# 設定頁面配置
st.set_page_config(
    page_title="台灣鳥類辨識器",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 樣式
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
    }
    .confidence-high {
        color: #2E7D32;
        font-weight: bold;
    }
    .confidence-medium {
        color: #F57C00;
        font-weight: bold;
    }
    .confidence-low {
        color: #D32F2F;
        font-weight: bold;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """載入訓練好的模型"""
    model_path = '../models/bird_classifier.keras'
    
    # 如果模型不存在，嘗試載入 H5 格式
    if not os.path.exists(model_path):
        model_path = '../models/bird_classifier.h5'
    
    if os.path.exists(model_path):
        try:
            model = keras.models.load_model(model_path)
            return model, None
        except Exception as e:
            return None, f"載入模型時發生錯誤: {str(e)}"
    else:
        return None, "找不到模型檔案，請先訓練模型"


def preprocess_image(image, target_size=(224, 224)):
    """
    預處理圖片
    """
    # 轉換為 RGB（如果是 RGBA 或其他格式）
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 調整大小
    image = image.resize(target_size)
    
    # 轉換為陣列並正規化
    img_array = np.array(image) / 255.0
    
    # 增加批次維度
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def predict_bird(model, image, class_names):
    """
    預測鳥類種類
    """
    # 預處理圖片
    processed_image = preprocess_image(image)
    
    # 預測
    predictions = model.predict(processed_image, verbose=0)
    
    # 取得預測結果
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx]
    predicted_class = class_names[predicted_class_idx]
    
    # 所有類別的機率
    probabilities = {class_names[i]: float(predictions[0][i]) 
                    for i in range(len(class_names))}
    
    return predicted_class, confidence, probabilities


def get_confidence_color(confidence):
    """根據信心度返回顏色類別"""
    if confidence >= 0.8:
        return "confidence-high"
    elif confidence >= 0.5:
        return "confidence-medium"
    else:
        return "confidence-low"


def get_bird_info(bird_name):
    """
    取得鳥類資訊
    """
    bird_info = {
        "白尾八哥": {
            "學名": "Acridotheres javanicus",
            "英文名": "Javan Myna",
            "特徵": "全身大致為黑褐色，尾下覆羽白色，飛行時可見白色尾端。",
            "分佈": "原產於爪哇，台灣為外來種，主要分佈在西部平地。",
            "習性": "群棲性強，常見於都市、農田環境。"
        },
        "家八哥": {
            "學名": "Acridotheres tristis",
            "英文名": "Common Myna",
            "特徵": "頭至胸部黑色，腹部褐色，眼周裸皮黃色，飛行時翼有白斑。",
            "分佈": "原產於南亞，台灣為外來種，廣泛分佈於平地至低海拔。",
            "習性": "適應力強，常見於都市、公園、農田。"
        },
        "林八哥": {
            "學名": "Acridotheres grandis",
            "英文名": "Great Myna",
            "特徵": "體型較大，全身黑色，頭部有羽冠，腳黃色。",
            "分佈": "原產於中國南方，台灣為外來種，主要在西部平地。",
            "習性": "喜棲息於樹林、農田，群棲性。"
        }
    }
    
    return bird_info.get(bird_name, None)


def main():
    # 標題
    st.markdown('<h1 class="main-header">🦜 台灣鳥類辨識器</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">使用遷移式學習識別台灣常見八哥科鳥類</p>', unsafe_allow_html=True)
    
    # 載入模型
    model, error = load_model()
    
    if error:
        st.error(error)
        st.info("請先執行訓練程式或 Jupyter Notebook 來訓練模型")
        st.stop()
    
    # 類別名稱（需與訓練時一致）
    class_names = ['白尾八哥', '家八哥', '林八哥']
    
    # 側邊欄
    with st.sidebar:
        st.header("ℹ️ 使用說明")
        st.markdown("""
        ### 如何使用
        1. 📤 上傳鳥類照片
        2. 🤖 AI 自動辨識
        3. 📊 查看預測結果
        
        ### 支援的鳥類
        - 🦜 白尾八哥
        - 🦜 家八哥
        - 🦜 林八哥
        
        ### 模型資訊
        - **架構**: MobileNetV2 (遷移式學習)
        - **輸入大小**: 224x224
        - **準確率**: ~85%+
        """)
        
        st.markdown("---")
        st.markdown("### 🔗 相關連結")
        st.markdown("- [GitHub Repository](https://github.com)")
        st.markdown("- [炎龍老師 AI-Demo](https://github.com/yenlung/AI-Demo)")
    
    # 主要內容區域
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 上傳圖片")
        
        # 檔案上傳
        uploaded_file = st.file_uploader(
            "選擇鳥類照片",
            type=['png', 'jpg', 'jpeg'],
            help="支援 PNG, JPG, JPEG 格式"
        )
        
        # 或使用範例圖片
        st.markdown("---")
        st.markdown("**或使用範例圖片**")
        use_example = st.button("🎲 使用隨機範例")
        
        if uploaded_file is not None:
            # 顯示上傳的圖片
            image = Image.open(uploaded_file)
            st.image(image, caption="上傳的圖片", use_container_width=True)
            
            # 圖片資訊
            st.caption(f"圖片大小: {image.size[0]} x {image.size[1]}")
            st.caption(f"格式: {image.format}")
            
    with col2:
        st.subheader("🎯 辨識結果")
        
        if uploaded_file is not None:
            with st.spinner("🔍 正在辨識中..."):
                # 進行預測
                predicted_class, confidence, probabilities = predict_bird(
                    model, image, class_names
                )
            
            # 顯示預測結果
            confidence_class = get_confidence_color(confidence)
            
            st.markdown(f"""
            <div class="prediction-box">
                <h2 style="margin: 0;">預測結果: {predicted_class}</h2>
                <p style="margin: 0.5rem 0 0 0;">
                    信心度: <span class="{confidence_class}">{confidence:.2%}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # 信心度建議
            if confidence >= 0.8:
                st.success("✅ 高信心度預測！結果可靠。")
            elif confidence >= 0.5:
                st.warning("⚠️ 中等信心度，建議參考其他照片確認。")
            else:
                st.error("❌ 低信心度，可能不是訓練過的鳥類或照片品質不佳。")
            
            # 顯示所有類別的機率
            st.markdown("### 📊 各類別預測機率")
            
            # 排序機率
            sorted_probs = sorted(probabilities.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
            
            for bird, prob in sorted_probs:
                st.progress(float(prob))
                st.caption(f"{bird}: {prob:.2%}")
            
            # 顯示鳥類資訊
            st.markdown("---")
            bird_info = get_bird_info(predicted_class)
            
            if bird_info:
                st.markdown(f"### 🐦 關於 {predicted_class}")
                with st.expander("查看詳細資訊", expanded=True):
                    st.markdown(f"**學名**: {bird_info['學名']}")
                    st.markdown(f"**英文名**: {bird_info['英文名']}")
                    st.markdown(f"**特徵**: {bird_info['特徵']}")
                    st.markdown(f"**分佈**: {bird_info['分佈']}")
                    st.markdown(f"**習性**: {bird_info['習性']}")
        else:
            st.info("👈 請從左側上傳鳥類照片開始辨識")
            
            # 顯示範例
            st.markdown("### 📷 範例照片")
            st.markdown("""
            上傳清晰的鳥類照片可以獲得更好的辨識效果：
            - ✅ 鳥類主體清晰
            - ✅ 光線充足
            - ✅ 適當的拍攝距離
            - ❌ 避免模糊或過暗的照片
            """)
    
    # 底部資訊
    st.markdown("---")
    st.markdown("""
    <div class="info-box">
        <b>⚠️ 注意事項</b><br>
        • 本系統僅供教學示範使用<br>
        • 辨識準確度受照片品質影響<br>
        • 建議搭配專業鳥類圖鑑確認結果<br>
        • 資料來源: 參考炎龍老師 AI-Demo 專案
    </div>
    """, unsafe_allow_html=True)
    
    # 頁尾
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**開發**: IoT HW4 專案")
    with col2:
        st.markdown("**技術**: TensorFlow + Streamlit")
    with col3:
        st.markdown("**年份**: 2025")


if __name__ == "__main__":
    main()
