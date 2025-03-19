#!/usr/bin/env python3
# coding: utf-8

import socket
import json

HOST = '127.0.0.1'
PORT = 65432


def start_server():
    """
    启动服务器，等待客户端连接，接收房产信息并返回预测房价
    """

    # ============== 模型代码放在这里 ==============
    #
    # 例如:
    # model = load_model('my_regression_model.h5')
    # preprocessor = joblib.load('my_preprocessor.pkl')
    #
    # 这里先简单模拟一个固定预测结果:
    # predicted_price = <some_value>
    #
    # ==============================================

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

            # ============== 这里应该调用模型进行预测 ==============
            # 假设我们已经拿到了 predicted_price
            # 以下只是示例:
            predicted_price = 520000
            #
            # 真实情况:
            # new_processed = preprocessor.transform(pd.DataFrame([new_house]))
            # predicted_price = model.predict(new_processed)[0][0]
            #
            # ==============================================

            response_data = {"predicted_price": predicted_price}
            response_json = json.dumps(response_data)
            conn.sendall(response_json.encode('utf-8'))

        except Exception as e:
            print(f"Error processing request: {e}")
        finally:
            conn.close()
            print(f"Connection with {addr} closed.")


if __name__ == "__main__":
    start_server()
