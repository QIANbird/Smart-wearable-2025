import pandas as pd
from data_processing import sliding_window, extract_features

# 读取归一化后的数据文件
data_file = r"E:\Aalto\smart wearable\codes\Data_Collected\combined_data_normalized.csv"
df = pd.read_csv(data_file)

# 对数据进行滑动窗口切分，窗口大小300，步长100
windows, window_labels = sliding_window(df, window_size=300, step_size=100, label_col="Label")
print(f"切分出 {len(windows)} 个窗口。")

# 对每个窗口提取特征，保存到一个列表
features_list = []
for i, window in enumerate(windows):
    features = extract_features(window)
    features["Label"] = window_labels[i]
    features_list.append(features)

# 将所有窗口的特征转换为 DataFrame，并保存
features_df = pd.DataFrame(features_list)
output_file = r"E:\Aalto\smart wearable\codes\Data_Collected\features.csv"
features_df.to_csv(output_file, index=False)
print(f"窗口特征已保存到 {output_file}")
