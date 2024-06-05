import os
import requests
import time
import csv
from unidecode import unidecode
from datetime import datetime
dweet_url = "https://dweet.io/get/latest/dweet/for/To_1"
file_path = 'data.csv'

# Check if the file exists
file_exists = os.path.isfile(file_path)

# Open the file in 'w' mode if it exists, otherwise in 'a' mode
with open(file_path, mode='w' if not file_exists else 'a', encoding='utf-8', newline='') as file:
    # Write header only if the file is newly created
    if not file_exists:
        file.write("temperature, humidity, sound, gas, light, tinhtrang, timestamp\n")
    try:
        while True:
            try: 
                response = requests.get(dweet_url)
                if response.status_code == 200:
                    data = response.json()

                    # Lấy thời gian hiện tại
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(data)
                    temperature = data['with'][0]['content']['temperature']
                    humidity = data['with'][0]['content']['humidity']
                    sound = data['with'][0]['content']["sound"]
                    gas = data['with'][0]['content']["gas"]
                    light = data['with'][0]['content']["light"]
                    tinhtrang = []

                    def normalize_label(label):
                        return unidecode(label).lower()

                    if int(temperature) > 30:
                        tinhtrang.append("Nhiệt độ Cao")
                    elif int(temperature) < 18:
                        tinhtrang.append("Nhiệt độ Thấp")
                    else:
                        tinhtrang.append("Nhiệt độ Bình thường")

                    # Gán nhãn cho Độ ẩm
                    if int(humidity) > 80:
                        tinhtrang.append("Phòng ẩm")
                    elif int(humidity) < 60:
                        tinhtrang.append("Phòng khô")
                    else:
                        tinhtrang.append("Độ ẩm ổn định")

                    # Gán nhãn cho Âm thanh
                    if int(sound) > 600:
                        tinhtrang.append("Ồn")
                    elif int(sound) < 350:
                        tinhtrang.append("Im lặng")
                    else:
                        tinhtrang.append("Bình thường")

                    # Gán nhãn cho Gas
                    if int(gas) <50:
                        tinhtrang.append("Khí bình thường")
                    elif 50<=int(gas)<=150:
                        tinhtrang.append("Nồng độ CO2 trung bình")
                    else:
                        tinhtrang.append("Nồng độ CO2 cao")

                    # Gán nhãn cho Light
                    if int(light) < 650:
                        tinhtrang.append("Sáng")
                    elif 650 <= int(light) < 2000:
                        tinhtrang.append("Ánh sáng bình thường")
                    else:
                        tinhtrang.append("Tối")

                    # Chuyển list thành một chuỗi, phân tách bằng dấu cộng
                    tinhtrang_string = '+'.join(tinhtrang)

                    
                    writer = csv.writer(file)
                    writer.writerow([temperature, humidity, sound, gas, light, tinhtrang_string, timestamp])
                    file.flush()
                    print(f"Timestamp: {timestamp}")
                    print(f"Nhiệt độ:  - Giá trị: {temperature}°C")
                    print(f"Độ ẩm:  - Giá trị: {humidity}%")
                    print(f"Âm thanh:  - Giá trị: {sound}")
                    print(f"Gas:  - Giá trị: {gas}")
                    print(f"Light:  - Giá trị: {light}")
                    time.sleep(3)
                else:
                    print("Không thể kết nối!")
            except KeyError as e:
                        print(f"KeyError: {e}. Could not extract data from JSON response.")
                        # Handle the error gracefully, e.g., continue to the next iteration or take appropriate action
                        time.sleep(5)
    except KeyboardInterrupt:
        print("\nĐã dừng ghi data vào file.")
