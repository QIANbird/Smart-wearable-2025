import pandas as pd
import glob
import os

# 设置存放数据的文件夹路径
data_dir = r"E:\Aalto\smart wearable\codes\Data_Collected"

# 定义各个姿势的文件名模式以及对应的标签
groups = {
    "tiptoe": "tiptoe_*_Xie.csv",
    "bottomup": "bottomup_*_Xie.csv",
    "leftup": "leftup_*_Xie.csv",
    "rightup": "rightup_*_Xie.csv",
    "stop": "stop_*_Xie.csv",
    "zero": "zeroCalibration_Xie.csv"  # 零基准数据集
}

# 用于存储各个文件读取后的DataFrame
df_list = []

# 遍历每个组
for label, pattern in groups.items():
    file_pattern = os.path.join(data_dir, pattern)
    file_list = glob.glob(file_pattern)

    # 如果某个模式没有匹配到文件（例如零基准只有一个文件），也能处理
    if not file_list:
        print(f"没有找到匹配的文件: {pattern}")
        continue

    # 对于匹配到的每个文件，读取数据，并添加一个新列"Label"
    for file in file_list:
        df_temp = pd.read_csv(file)
        df_temp["Label"] = label  # 添加标签列
        # 可选：记录文件名
        df_temp["FileName"] = os.path.basename(file)
        df_list.append(df_temp)

# 将所有DataFrame合并成一个
combined_df = pd.concat(df_list, ignore_index=True)

# 将整合后的数据保存为新的CSV文件
output_file = os.path.join(data_dir, "combined_data.csv")
combined_df.to_csv(output_file, index=False)

print(f"数据整合完成，合并后的数据保存为：{output_file}")
