"""
訓練腳本 - 鳥類辨識器
使用遷移式學習訓練模型
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import os

# 設定參數
TRAIN_DIR = 'data/train'
TEST_DIR = 'data/test'
MODEL_SAVE_PATH = 'models/bird_classifier.keras'
IMG_SIZE = 224
BATCH_SIZE = 8  # Reduced for small dataset
EPOCHS = 50  # Increased for better convergence
LEARNING_RATE = 0.0001
NUM_CLASSES = 3

print("=" * 60)
print("台灣鳥類辨識器 - 模型訓練")
print("=" * 60)
print(f"TensorFlow 版本: {tf.__version__}")
print(f"Keras 版本: {keras.__version__}")
print()

# 檢查訓練資料是否存在
if not os.path.exists(TRAIN_DIR):
    print(f"錯誤: 找不到訓練資料夾 {TRAIN_DIR}")
    print("請先執行 prepare_data.py 準備訓練資料")
    exit(1)

# 資料生成器
print("準備資料生成器...")
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

test_datagen = ImageDataGenerator(rescale=1./255)

# 載入訓練和驗證資料
print("載入訓練資料...")
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

print(f"訓練集圖片數量: {train_generator.samples}")
print(f"驗證集圖片數量: {validation_generator.samples}")
print(f"類別: {list(train_generator.class_indices.keys())}")
print()

# 建立模型
print("建立遷移式學習模型...")
base_model = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

# 凍結基礎模型
base_model.trainable = False

# 建立完整模型
inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base_model(inputs, training=False)
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(NUM_CLASSES, activation='softmax')(x)

model = Model(inputs, outputs)

# 編譯模型
print("編譯模型...")
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print()
model.summary()
print()

# 回調函數
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-7
    ),
    keras.callbacks.ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_accuracy',
        save_best_only=True,
        verbose=1
    )
]

# 訓練模型
print("=" * 60)
print("開始訓練...")
print("=" * 60)

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=callbacks
)

print()
print("=" * 60)
print("訓練完成！")
print("=" * 60)

# 顯示最終結果
final_train_acc = history.history['accuracy'][-1]
final_val_acc = history.history['val_accuracy'][-1]
print(f"最終訓練準確率: {final_train_acc:.4f}")
print(f"最終驗證準確率: {final_val_acc:.4f}")

# 儲存模型
print()
print(f"儲存模型至: {MODEL_SAVE_PATH}")
os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
model.save(MODEL_SAVE_PATH)

# 也儲存成 H5 格式
h5_path = MODEL_SAVE_PATH.replace('.keras', '.h5')
model.save(h5_path)
print(f"模型也儲存成 H5 格式: {h5_path}")

# 繪製訓練曲線
print()
print("繪製訓練曲線...")
plt.figure(figsize=(14, 5))

# 準確率
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='訓練準確率')
plt.plot(history.history['val_accuracy'], label='驗證準確率')
plt.title('模型準確率')
plt.xlabel('Epoch')
plt.ylabel('準確率')
plt.legend()
plt.grid(True)

# 損失
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='訓練損失')
plt.plot(history.history['val_loss'], label='驗證損失')
plt.title('模型損失')
plt.xlabel('Epoch')
plt.ylabel('損失')
plt.legend()
plt.grid(True)

plt.tight_layout()
plot_path = 'models/training_history.png'
plt.savefig(plot_path)
print(f"訓練曲線已儲存至: {plot_path}")

print()
print("=" * 60)
print("所有工作完成！")
print("=" * 60)
print()
print("接下來可以：")
print("1. 執行 streamlit run app.py 啟動網頁應用")
print("2. 測試模型預測效果")
print("3. 部署到 Streamlit Cloud")
