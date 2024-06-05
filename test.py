import pyodbc
from keras.models import load_model
import numpy as np
import requests
import joblib
import os
import csv
import time
from datetime import datetime
from unidecode import unidecode
#học máy
loaded_model = load_model('trained_model.h5')

file_path = 'data.csv'
# Sample Dweet URL, replace it with your actual URL
dweet_url = "https://dweet.io/get/latest/dweet/for/To_1"
# Thông tin kết nối SQL Server
server_name = 'DESKTOP-FF9VATI'
database_name = 'Iot_Data1'

username = ''
password = ''


# Kết nối đến SQL Server
conn = pyodbc.connect(
    f'DRIVER={{SQL Server}};'
    f'SERVER={server_name};'
    f'DATABASE={database_name};'
    f'UID={username};'
    f'PWD={password};'
)
file_exists = os.path.isfile(file_path)

cursor = conn.cursor()
#giải mã file training qua file encoder
encoder = joblib.load('label_encoder.joblib')

with open(file_path, mode='w' if not file_exists else 'a', encoding='utf-8', newline='') as file:
    # Write header only if the file is newly created
    if not file_exists:
        file.write("temperature, humidity, sound, gas, light, tinhtrang, timestamp\n")
    try:
        while True:
            try:
                #phản hồi
                response = requests.get(dweet_url)
                if response.status_code == 200:
                    data = response.json()
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    temperature = data['with'][0]['content']['temperature']
                    humidity = data['with'][0]['content']['humidity']
                    sound = data['with'][0]['content']["sound"]
                    gas = data['with'][0]['content']["gas"]
                    light = data['with'][0]['content']["light"]

                    new_test_data = np.array([temperature, humidity, sound, gas, light])
                    new_test_data = new_test_data.reshape(1, -1)

                    # Select the first 5 columns (index 0 to 4) and convert to float
                    new_x = new_test_data[:, :5].astype(float)

                    # Make predictions
                    predicted_probabilities = loaded_model.predict(new_x)

                    # Chuyển đổi kết quả về nhãn ban đầu
                    predicted_labels = encoder.inverse_transform(predicted_probabilities)

                    # Hiển thị kết quả
                    predicted_labels_1d = predicted_labels.flatten()

                    # Thay thế dấu cộng thành dấu phẩy
                    predicted_labels_str = str(predicted_labels_1d[0]).replace('+', ',')
                    
                    # Hiển thị kết quả
                    predicted_labels_array = predicted_labels_str.split(',')
                    print(predicted_labels_array)

                    

                    # Function to remove accents and convert to lowercase
                    def normalize_label(label):
                        return unidecode(label).lower()

                    # ...

                    # Gán nhãn cho Nhiệt độ
                    if temperature == 'nan':
                        print("Chỉnh lại cảm biến")
                        time.sleep(5)
                        
                    elif temperature > 30:
                        nhiet_do_label = normalize_label("Cao")
                    elif temperature < 18:
                        nhiet_do_label = normalize_label("Thấp")
                    else:
                        nhiet_do_label = normalize_label("Bình thường")

                    # Gán nhãn cho Độ ẩm
                    if humidity == 'nan':
                        print("Chỉnh lại cảm biến")
                        time.sleep(5)
                    elif humidity > 80:
                        do_am_label = normalize_label("Phòng ẩm")
                    elif humidity < 60:
                        do_am_label = normalize_label("Phòng khô")
                    else:
                        do_am_label = normalize_label("Bình thường")

                    # Gán nhãn cho Âm thanh
                    if int(sound) > 600:
                        am_thanh_label = normalize_label("Ồn")
                    elif int(sound) < 400:
                        am_thanh_label = normalize_label("Im lặng")
                    else:
                        am_thanh_label = normalize_label("Bình thường")

                    # Gán nhãn cho Gas
                    if gas <50:
                        gas_label = normalize_label("Khí bình thường")
                    elif 50<=gas<150:
                        gas_label = normalize_label("Nồng độ CO trung bình")
                    else:
                        gas_label = normalize_label("Nồng độ CO2 cao")

                    # Gán nhãn cho Light
                    if int(light) < 650:
                        light_label = normalize_label("Sáng")
                    elif 650 <= int(light) < 2000:
                        light_label = normalize_label("Ánh sáng bình thường")
                    else:
                        light_label = normalize_label("Tối")

                    print(f"Timestamp: {timestamp}")
                    print(f"Nhiệt độ:  - Giá trị: {temperature}°C")
                    print(f"Độ ẩm:  - Giá trị: {humidity}%")
                    print(f"Âm thanh:  - Giá trị: {sound}")
                    print(f"Gas:  - Giá trị: {gas}")
                    print(f"Light:  - Giá trị: {light}")

                    
                    writer = csv.writer(file)
                    writer.writerow([temperature, humidity, sound, gas, light, str(predicted_labels_1d[0]), timestamp])
                    file.flush()
                    #Đẩy dữ liệu lên SQL server với bảng Preditions
                    query = "INSERT INTO Predictions (Label1, Label2, Label3, Label4, Label5) VALUES (?, ?, ?, ?, ?)"
                    cursor.execute(query, predicted_labels_array)

                    # Xử lý dữ liệu và cập nhật vào cơ sở dữ liệu SQL Server
                    cursor.execute("INSERT INTO NhietDo (giaTri, nhan, thoiGian) VALUES (?, ?, ?)", (temperature, nhiet_do_label, timestamp))
                    cursor.execute("INSERT INTO DoAm (giaTri, nhan, thoiGian) VALUES (?, ?, ?)", (humidity, do_am_label, timestamp))
                    cursor.execute("INSERT INTO AmThanh (giaTri, nhan, thoiGian) VALUES (?, ?, ?)", (sound, am_thanh_label, timestamp))
                    cursor.execute("INSERT INTO Gas (giaTri, nhan, thoiGian) VALUES (?, ?, ?)", (gas, gas_label, timestamp))
                    cursor.execute("INSERT INTO AnhSang (giaTri, nhan, thoiGian) VALUES (?, ?, ?)", (light, light_label, timestamp))
                    # Commit để lưu thay đổi vào cơ sở dữ liệu
                    conn.commit()
                    print("Dữ liệu đã được cập nhật vào SQL Server." + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    time.sleep(5)
                
                else:
                    print("Không thể kết nối!")
            except KeyError as e:
                print(f"KeyError: {e}. Could not extract data from JSON response.")
                # Handle the error gracefully, e.g., continue to the next iteration or take appropriate action
                time.sleep(5)
    except KeyboardInterrupt:
        print("\nĐã dừng cập nhật dữ liệu vào SQL Server.")

# Đóng kết nối
cursor.close()
conn.close()
