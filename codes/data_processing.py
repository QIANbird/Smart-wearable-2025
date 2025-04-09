import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle
import os


def normalize_data(input_csv, output_csv, scaler_file, sensor_keywords=["Voltage", "Resistance"]):
    """
    读取CSV文件，对指定的传感器数据列进行归一化处理，
    保存归一化后的数据以及归一化器到文件中。
    参数：
      input_csv: 原始CSV文件路径
      output_csv: 保存归一化后数据的路径
      scaler_file: 保存归一化器（scaler）的文件路径
      sensor_keywords: 用于选择需要归一化的列的关键词列表
    返回：
      df: 归一化后的DataFrame
    """
    df = pd.read_csv(input_csv)
    # 筛选包含传感器数据的列
    sensor_cols = [col for col in df.columns if any(keyword in col for keyword in sensor_keywords)]

    scaler = MinMaxScaler()
    df[sensor_cols] = scaler.fit_transform(df[sensor_cols])

    # 保存归一化器以便实时检测时复用
    with open(scaler_file, "wb") as f:
        pickle.dump(scaler, f)

    # 保存归一化后的数据
    df.to_csv(output_csv, index=False)
    print(f"数据归一化完成，结果保存为 {output_csv}")
    return df


def zero_baseline_calibration(df, sensor_keywords=["Voltage", "Resistance"],
                              baseline_filename="zeroCalibration_Xie.csv", file_col="FileName"):
    """
    对归一化后的数据进行零基线校准：筛选出基线数据（file_col列等于 baseline_filename），
    计算各传感器的基线平均值，再将整个数据集的传感器数据减去该基线值。

    参数：
      df: 归一化后的DataFrame
      sensor_keywords: 用于筛选传感器数据的关键词列表
      baseline_filename: 表示零基线数据的文件名
      file_col: 数据中表示原始文件名的列名
    返回：
      df_calibrated: 校准后的DataFrame
    """
    sensor_cols = [col for col in df.columns if any(keyword in col for keyword in sensor_keywords)]
    baseline_df = df[df[file_col] == baseline_filename]

    if baseline_df.empty:
        print(f"未找到基线数据，FileName列中无 '{baseline_filename}'。")
        return df

    # 计算基线平均值（可以改用中位数）
    baseline_values = baseline_df[sensor_cols].mean()
    print("各传感器基线平均值：")
    print(baseline_values)

    df_calibrated = df.copy()
    df_calibrated[sensor_cols] = df_calibrated[sensor_cols] - baseline_values
    return df_calibrated


def sliding_window(data, window_size=300, step_size=100, label_col="Label"):
    """
    对输入的 DataFrame 数据进行滑动窗口切分。

    参数：
      data: pd.DataFrame，包含所有数据和标签
      window_size: int，每个窗口的采样点数（默认为300）
      step_size: int，窗口滑动步长（默认为100）
      label_col: str，表示标签列的列名
    返回：
      windows: list，每个元素为一个DataFrame窗口
      window_labels: list，每个窗口对应的标签（采用该窗口中出现次数最多的标签）
    """
    windows = []
    window_labels = []
    for start in range(0, len(data) - window_size + 1, step_size):
        end = start + window_size
        window = data.iloc[start:end].copy()
        windows.append(window)
        if label_col in data.columns:
            label = window[label_col].mode()[0]
        else:
            label = None
        window_labels.append(label)
    return windows, window_labels


def extract_features(window, sensor_keywords=["Voltage", "Resistance"]):
    """
    从单个窗口中提取特征，这里以每个传感器数据的均值和标准差为例。

    参数：
      window: pd.DataFrame，单个窗口数据
      sensor_keywords: 用于筛选传感器数据列的关键词列表
    返回：
      features: dict，包含特征名称和对应的值
    """
    features = {}
    sensor_cols = [col for col in window.columns if any(keyword in col for keyword in sensor_keywords)]
    for col in sensor_cols:
        features[f"{col}_mean"] = window[col].mean()
        features[f"{col}_std"] = window[col].std()
    return features