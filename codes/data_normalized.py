import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 读取整合后的数据（假设文件名为 combined_data.csv）
df = pd.read_csv(r"E:\Aalto\smart wearable\codes\Data_processed\combined_data.csv")

# 查看数据列名，假设包含 "S1_Voltage", "S2_Voltage", …, "S6_Voltage" 以及 "S1_Resistance", …, "S6_Resistance"
print("原始数据列：", df.columns)

# 选择需要归一化的列（这里假设电压和电阻数据都需要归一化）
sensor_cols = [col for col in df.columns if "Voltage" in col or "Resistance" in col]

# 如果你希望基于零基准校准数据先减去基线值，也可以在这里进行相应调整
# 例如：df[sensor_cols] = df[sensor_cols] - baseline_value

# 初始化归一化器，将数据缩放到 [0, 1] 范围内
scaler = MinMaxScaler()

# 对选中的列进行归一化处理
df[sensor_cols] = scaler.fit_transform(df[sensor_cols])

# 可选：如果需要将归一化参数保存下来，以便实时系统中使用相同的归一化方法，可以保存 scaler
import pickle
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

# 保存归一化后的数据到新文件
df.to_csv(r"E:\Aalto\smart wearable\codes\Data_processed\combined_data_normalized.csv", index=False)
print("数据归一化完成，结果保存为 combined_data_normalized.csv")
