import pandas as pd
import os
from data_processing import normalize_data, zero_baseline_calibration, sliding_window, extract_features

base_dir = r"E:\Aalto\smart wearable\codes\Data_processed"
input_csv = os.path.join(base_dir, "combined_data.csv")
normalized_csv = os.path.join(base_dir, "combined_data_normalized.csv")
scaler_file = os.path.join(base_dir, "scaler.pkl")

# 1. 数据归一化
df_normalized = normalize_data(input_csv, normalized_csv, scaler_file)

# 2. 零基线校准（使用FileName列中标记的零基线数据）
df_calibrated = zero_baseline_calibration(df_normalized)
calibrated_csv = os.path.join(base_dir, "combined_data_normalized_calibrated.csv")
df_calibrated.to_csv(calibrated_csv, index=False)
print(f"零基线校准完成，结果保存为 {calibrated_csv}")

# 3. 滑动窗口切分
windows, window_labels = sliding_window(df_calibrated, window_size=300, step_size=100, label_col="Label")
print(f"切分出 {len(windows)} 个窗口")

# 4. 特征提取：对每个窗口提取特征，并生成一个总的特征DataFrame
features_list = []
for i, window in enumerate(windows):
    features = extract_features(window)
    features["Label"] = window_labels[i]
    features_list.append(features)

features_df = pd.DataFrame(features_list)
features_csv = os.path.join(base_dir, "features.csv")
features_df.to_csv(features_csv, index=False)
print(f"窗口特征已保存到 {features_csv}")