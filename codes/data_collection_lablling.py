import serial
import json
import csv
import time
import keyboard  # 需要安装：pip install keyboard

# Serial Port Configuration (Modify for your OS)
SERIAL_PORT = "COM5"  # Use 'COMx' for Windows
BAUD_RATE = 115200
#收集数据，存储到各自不同的文件
CSV_FILE =r"E:\Aalto\smart wearable\codes\Data_Collected\stop_08_Xie.csv"
# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Open CSV file for writing
with open(CSV_FILE, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    # 加入 "Label" 列
    csv_writer.writerow(["Time(ms)", "S1_Voltage", "S2_Voltage", "S3_Voltage", "S4_Voltage", "S5_Voltage", "S6_Voltage",
                         "S1_Resistance", "S2_Resistance", "S3_Resistance", "S4_Resistance", "S5_Resistance",
                         "S6_Resistance", "Label"])

    t_start = None  # 用于调整时间戳，来自传感器数据
    sample_count = 0  # 替代时间计数器（可选）
    sampling_rate = 10  # 采样间隔，单位毫秒
    start_time = time.time()  # 记录采集开始时间

    try:
        while True:
            # 检查是否已采集 10 秒的数据
            if time.time() - start_time >= 10:
                print("10秒采样完成。")
                break

            line = ser.readline().decode("utf-8").strip()
            if not line:
                continue

            try:
                data = json.loads(line)  # 解析 JSON 数据
                time_stamp = data["time"]  # 从 Arduino 获取时间戳

                # 第一次采集时记录 t_start
                if t_start is None:
                    t_start = time_stamp

                # 调整时间，使得第一条数据为 0
                time_adj = time_stamp - t_start

                voltages = data["voltages"]
                resistances = data["resistances"]

                # 根据实时按键检测赋予标签：
                # 按 '0' -> "transition"，按 '1' -> "action"，否则 "zero"
                if keyboard.is_pressed('0'):
                    label = "transition"
                elif keyboard.is_pressed('1'):
                    label = "action"
                else:
                    label = "zero"

                # 将数据和标签写入 CSV
                csv_writer.writerow([time_adj] + voltages + resistances + [label])
                print(f"Saved: {time_adj} ms, Voltages: {voltages}, Resistances: {resistances}, Label: {label}")

                sample_count += 1  # 增加样本计数

            except json.JSONDecodeError:
                print("Invalid JSON received, skipping...")

            time.sleep(sampling_rate / 1000)  # 保持正确采样间隔

    except KeyboardInterrupt:
        print("\nStopping data logging...")

    ser.close()
