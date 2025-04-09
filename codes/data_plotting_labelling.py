import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of files to process
file_paths = [
    r"E:\Aalto\smart wearable\codes\Data_Collected\rightup_03_Xie.csv"
]

fs = 100  # Sampling frequency in Hz
dt = 1 / fs  # Time step

for file_path in file_paths:
    try:
        # Load the data
        df = pd.read_csv(file_path)

        # 使用 CSV 中的 "Time(ms)" 列构造时间向量，转换为秒
        if "Time(ms)" in df.columns:
            time = df["Time(ms)"].astype(float) / 1000.0
        else:
            time = np.arange(len(df)) * dt

        # 假设你想绘制的是各个传感器的 Resistance 数据
        # 列顺序：[S1_Resistance, S2_Resistance, ..., S6_Resistance]，即第8列到倒数第2列（最后一列是 Label）
        sensor_data = df.iloc[:, 7:-1]  # 提取 S1_Resistance 到 S6_Resistance

        # 计算标准差（可选）
        std_devs = sensor_data.std()
        print(f"Standard deviations for {file_path}:")
        print(std_devs)
        print("-" * 50)

        # Define custom legend labels for resistance sensors
        legend_labels = [f"Sensor {i + 1}" for i in range(sensor_data.shape[1])]

        # 绘图
        plt.figure(figsize=(10, 6))
        # 绘制每个传感器的信号（单位转换，根据实际情况调整）
        for col, label in zip(sensor_data.columns, legend_labels):
            plt.plot(time, sensor_data[col] / 1000, label=label)

        # 根据 Label 列添加背景色显示各阶段
        if "Label" in df.columns:
            # 将连续相同的 Label 分组
            df['Group'] = (df['Label'] != df['Label'].shift()).cumsum()

            # 定义各阶段背景色
            label_colors = {
                "zero": "lightgrey",
                "action": "lightgreen",
                "transition": "lightblue"
            }
            added_labels = set()  # 控制图例中每个标签只显示一次

            # 对每个分组绘制背景色
            for group_id, group_data in df.groupby("Group"):
                phase = group_data["Label"].iloc[0]
                # 使用 Time(ms) 列获取该分段的起始和结束时间（转换为秒）
                if "Time(ms)" in df.columns:
                    t_start = group_data["Time(ms)"].iloc[0] / 1000.0
                    t_end = group_data["Time(ms)"].iloc[-1] / 1000.0
                else:
                    t_start = group_data.index[0] * dt
                    t_end = group_data.index[-1] * dt

                if phase in label_colors:
                    if phase not in added_labels:
                        plt.axvspan(t_start, t_end, facecolor=label_colors[phase], alpha=0.3, label=phase)
                        added_labels.add(phase)
                    else:
                        plt.axvspan(t_start, t_end, facecolor=label_colors[phase], alpha=0.3)

        plt.xlabel("Time [s]")
        plt.ylabel("Resistance [kOhm]")
        plt.title(f"Sensor Data for {os.path.basename(file_path)}")
        plt.legend(loc="upper right")
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
