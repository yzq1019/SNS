#!/usr/bin/env python3
# coding: utf-8

import socket
import json

HOST = '127.0.0.1'
PORT = 65432

def prompt_for_int(prompt_text):
    """
    帮助函数：提示用户输入数字，并进行简单的int转换
    如果转换失败会再次提示
    """
    while True:
        user_input = input(prompt_text).strip()
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")

def main():
    print("Hello, I'm the Oracle. How can I help you today?")
    print("Let's collect 18 pieces of information to predict your house price.")

    # 与训练时保持一致的特征字段
    # 注意哪些是数字型特征，需要 int() 转换
    address          = input("1) Address: ")
    neighborhood     = input("2) Neighborhood: ")
    bedrooms         = prompt_for_int("3) Bedrooms (integer): ")
    bathrooms        = prompt_for_int("4) Bathrooms (integer): ")
    square_meters    = prompt_for_int("5) Square Meters (integer): ")
    building_age     = prompt_for_int("6) Building Age (integer): ")
    garden           = prompt_for_int("7) Garden? (1 for Yes, 0 for No): ")
    garage           = prompt_for_int("8) Garage? (1 for Yes, 0 for No): ")
    floors           = prompt_for_int("9) Floors (integer): ")
    property_type    = input("10) Property Type (e.g. Flat, House): ")
    heating_type     = input("11) Heating Type (e.g. Central): ")
    balcony          = input("12) Balcony (Yes/No): ")
    interior_style   = input("13) Interior Style (e.g. Modern): ")
    view             = input("14) View (e.g. Street): ")
    materials        = input("15) Materials (e.g. Brick): ")
    building_status  = input("16) Building Status (e.g. Completed): ")
    no_receptions    = prompt_for_int("17) No. of Receptions (integer): ")
    postal_code      = input("18) Postal Code (e.g. NW1 0NE): ")

    # 将用户输入组装成字典，用于后续传输给服务器进行数据处理
    new_house = {
        'Address': address,
        'Neighborhood': neighborhood,
        'Bedrooms': bedrooms,
        'Bathrooms': bathrooms,
        'Square Meters': square_meters,
        'Building Age': building_age,
        'Garden': garden,
        'Garage': garage,
        'Floors': floors,
        'Property Type': property_type,
        'Heating Type': heating_type,
        'Balcony': balcony,
        'Interior Style': interior_style,
        'View': view,
        'Materials': materials,
        'Building Status': building_status,
        'No. of Receptions': no_receptions,
        'Postal Code': postal_code
    }

    # 创建 TCP 客户端套接字并连接服务器
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"\nConnected to server {HOST}:{PORT}")

        # 发送 JSON 格式的数据
        request_json = json.dumps(new_house)
        client_socket.sendall(request_json.encode('utf-8'))

        # 接收服务器返回的预测结果
        response_data = client_socket.recv(4096)
        if response_data:
            response = json.loads(response_data.decode('utf-8'))
            predicted_price = response.get("predicted_price", "Unknown")
            print(f"\nThe predicted price for your house is: £{predicted_price:,}")
        else:
            print("No data received from server.")

    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        client_socket.close()
        print("Client connection closed.")

if __name__ == "__main__":
    main()
