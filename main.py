import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 重新加载训练集和验证集
train_path = 'C:/Users/49084/Desktop/London-pricepredict/input/london_train_data.csv'
val_path = 'C:/Users/49084/Desktop/London-pricepredict/input/london_validation_data.csv'

train_df = pd.read_csv(train_path)
val_df = pd.read_csv(val_path)

# 定义统一的预处理函数
def preprocess_data(df):
    # 去除冗余或无关列
    cols_to_drop = [
        'Unnamed: 0', 'price', 'Area in sq ft',
        'No.of Bedrooms', 'No. of Bathrooms',
        'Mapped_location', 'Property Name',
        'City/County', 'Location', 'House Type'
    ]
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

    # 保留建模需要的列
    selected_columns = [
        'Address','Neighborhood', 'Bedrooms', 'Bathrooms', 'Square Meters',
        'Building Age', 'Garden', 'Garage', 'Floors', 'Property Type',
        'Heating Type', 'Balcony', 'Interior Style', 'View', 'Materials',
        'Building Status', 'Price', 'No. of Receptions', 'Postal Code'
    ]
    df = df[selected_columns]

    return df

# 应用清洗函数
train_clean = preprocess_data(train_df)
val_clean = preprocess_data(val_df)

# 分离特征与标签
X_train = train_clean.drop(columns=['Price'])
y_train = train_clean['Price']

X_val = val_clean.drop(columns=['Price'])
y_val = val_clean['Price']

# 数值型和类别型特征
numerical_features = [
    'Bedrooms', 'Bathrooms', 'Square Meters', 'Building Age',
    'Garden', 'Garage', 'Floors', 'No. of Receptions'
]
categorical_features = [
    'Address','Neighborhood', 'Property Type', 'Heating Type', 'Balcony',
    'Interior Style', 'View', 'Materials', 'Building Status', 'Postal Code'
]

# 构建特征工程预处理器
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# 拟合训练集并转换训练/验证集
X_train_processed = preprocessor.fit_transform(X_train)
X_val_processed = preprocessor.transform(X_val)

# 输出处理后的形状信息
print("Numbers of Training set ：", X_train.shape[0])
print("Numbers of Training set Features：", X_train_processed.shape[1])
print("Numbers of Validation set：", X_val.shape[0])
print("Numbers of Validation set Features：", X_val_processed.shape[1])
print("Preprocess Success")


# 神经网络模型结构
model = Sequential([
    Dense(256, activation='relu', input_shape=(X_train_processed.shape[1],)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(1)
])

# 编译模型
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 早停防止过拟合
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
from tensorflow.keras.optimizers import Adam
model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
# 训练模型
model.fit(
    X_train_processed, y_train,
    validation_data=(X_val_processed, y_val),
    epochs=50,
    batch_size=64,  # 尝试更大的批量
    callbacks=[early_stop],
    verbose=1
)

# 预测验证集
y_pred = model.predict(X_val_processed).flatten()

# 模型评估
mae = mean_absolute_error(y_val, y_pred)
rmse = mean_squared_error(y_val, y_pred, squared=False)
r2 = r2_score(y_val, y_pred)

print(f"\n✅ 评估结果：")
print(f"MAE  : £{mae:.2f}")
print(f"RMSE : £{rmse:.2f}")
print(f"R²   : {r2:.4f}")


# 新房产样本（字典）
new_house = {
    'Address':'111',
    'Neighborhood': 'Camden',
    'Bedrooms': 3,
    'Bathrooms': 2,
    'Square Meters': 85,
    'Building Age': 5,
    'Garden': 1,
    'Garage': 0,
    'Floors': 2,
    'Property Type': 'Flat',
    'Heating Type': 'Central',
    'Balcony': 'Yes',
    'Interior Style': 'Modern',
    'View': 'Street',
    'Materials': 'Brick',
    'Building Status': 'Completed',
    'No. of Receptions': 1,
    'Postal Code': 'NW1 0NE'
}

# 转为 DataFrame（模型要求二维输入）
new_df = pd.DataFrame([new_house])

# 应用之前训练好的 preprocessor 进行编码 & 标准化
new_processed = preprocessor.transform(new_df)

# 预测房价
predicted_price = model.predict(new_processed)[0][0]
print(f"💰 预测房价：£{predicted_price:,.2f}")


