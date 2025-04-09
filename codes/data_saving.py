import serial
import json
import csv
import time

# Serial Port Configuration (Modify for your OS)
SERIAL_PORT = "COM7"  # Use 'COMx' for Windows
BAUD_RATE = 115200
CSV_FILE = "E:/Aalto/smart wearable/codes/Data_Collected/tiptoe_Xie_01.csv"

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

# Open CSV file for writing
with open(CSV_FILE, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Time(ms)", "S1_Voltage", "S2_Voltage", "S3_Voltage", "S4_Voltage", "S5_Voltage", "S6_Voltage",
                         "S1_Resistance", "S2_Resistance", "S3_Resistance", "S4_Resistance", "S5_Resistance",
                         "S6_Resistance"])

    t_start = None  # 用于调整时间戳，来自传感器数据
    sample_count = 0  # 替代时间计数器（可选）
    sampling_rate = 10  # 采样间隔，单位毫秒
    # 记录系统开始采样的时间（用于限定采样时长）
    start_time = time.time()

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

                # 调整时间，使得第一条数据为0
                time_adj = time_stamp - t_start

                voltages = data["voltages"]
                resistances = data["resistances"]

                # 写入调整后的时间和其他数据到 CSV
                csv_writer.writerow([time_adj] + voltages + resistances)
                print(f"Saved: {time_adj} ms, Voltages: {voltages}, Resistances: {resistances}")

                sample_count += 1  # 计数器增加

            except json.JSONDecodeError:
                print("Invalid JSON received, skipping...")

            time.sleep(sampling_rate / 1000)  # 保持正确采样间隔

    except KeyboardInterrupt:
        print("\nStopping data logging...")

    ser.close()
