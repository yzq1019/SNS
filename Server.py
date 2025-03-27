#!/usr/bin/env python3
# coding: utf-8

import socket
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, root_mean_squared_error


HOST = '127.0.0.1'
PORT = 65432

model = None
preprocessor = None

def train_and_init_model():
    global model, preprocessor

    # Read Tranining Set and Validation Set
    train_path = './london_train_data.csv'
    val_path = './london_validation_data.csv'

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)

    # Define Preprocessing Function
    def preprocess_data(df):
        # Delete useless Columns
        cols_to_drop = [
            'Unnamed: 0', 'price', 'Area in sq ft',
            'No.of Bedrooms', 'No. of Bathrooms',
            'Mapped_location', 'Property Name',
            'City/County', 'Location', 'House Type'
        ]
        df = df.drop(columns=[col for col in cols_to_drop if col in df.columns])

        # Keep useful Columns
        selected_columns = [
            'Address', 'Neighborhood', 'Bedrooms', 'Bathrooms', 'Square Meters',
            'Building Age', 'Garden', 'Garage', 'Floors', 'Property Type',
            'Heating Type', 'Balcony', 'Interior Style', 'View', 'Materials',
            'Building Status', 'Price', 'No. of Receptions', 'Postal Code'
        ]
        df = df[selected_columns]

        return df

    # Data Cleaning
    train_clean = preprocess_data(train_df)
    val_clean = preprocess_data(val_df)

    # Split Features
    X_train = train_clean.drop(columns=['Price'])
    y_train = train_clean['Price']

    X_val = val_clean.drop(columns=['Price'])
    y_val = val_clean['Price']

    
    numerical_features = [
        'Bedrooms', 'Bathrooms', 'Square Meters', 'Building Age',
        'Garden', 'Garage', 'Floors', 'No. of Receptions'
    ]
    categorical_features = [
        'Address', 'Neighborhood', 'Property Type', 'Heating Type', 'Balcony',
        'Interior Style', 'View', 'Materials', 'Building Status', 'Postal Code'
    ]

    # Building a Feature Engineering Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    # Fitting the training set and transforming the training/validation set
    X_train_processed = preprocessor.fit_transform(X_train)
    X_val_processed = preprocessor.transform(X_val)

    # Output of processed shape information
    print("Numbers of Training set ：", X_train.shape[0])
    print("Numbers of Training set Features：", X_train_processed.shape[1])
    print("Numbers of Validation set：", X_val.shape[0])
    print("Numbers of Validation set Features：", X_val_processed.shape[1])
    print("Preprocess Success")

    # Neural network model structure
    model = Sequential([
        Dense(256, activation='relu', input_shape=(X_train_processed.shape[1],)),
        Dropout(0.1),
        Dense(128, activation='relu'),
        Dropout(0.1),
        Dense(64, activation='relu'),
        Dropout(0.1),
        Dense(1)
    ])


    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    # Earlystop
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    from tensorflow.keras.optimizers import Adam
    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
    # Model Training
    model.fit(
        X_train_processed, y_train,
        validation_data=(X_val_processed, y_val),
        epochs=50,
        batch_size=64,  
        callbacks=[early_stop],
        verbose=1
    )

    # Prediction of Validation Set
    y_pred = model.predict(X_val_processed).flatten()

    # Model access
    mae = mean_absolute_error(y_val, y_pred)
    rmse = root_mean_squared_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)

    print(f"\n✅ Evaluation Result：")
    print(f"MAE  : £{mae:.2f}")
    print(f"RMSE : £{rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    # Save the Model
    model.save('house_price_model.keras')
    joblib.dump(preprocessor, 'preprocessor.pkl')





def start_server():
    """
    启动服务器，等待客户端连接，接收房产信息并返回预测房价
    """
    global model, preprocessor

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server is running on {HOST}:{PORT}, waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")

        try:
            data = conn.recv(4096)
            if not data:
                print("No data received, closing connection.")
                conn.close()
                continue

            # 将 JSON 字节解码并转换为 Python 字典
            new_house = json.loads(data.decode('utf-8'))
            # 用 preprocessor & model 进行预测
            df_new = pd.DataFrame([new_house])        # 转为 DataFrame
            X_new = preprocessor.transform(df_new)    # 特征工程
            y_pred = model.predict(X_new)[0][0]       # 预测值 (单个样本)


            response_data = {"predicted_price": float(y_pred)}
            response_json = json.dumps(response_data)
            conn.sendall(response_json.encode('utf-8'))

        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            conn.close()
            print(f"Connection with {addr} closed.")


if __name__ == "__main__":
    # 先训练并初始化模型
    train_and_init_model()

    # 再启动服务器
    start_server()
