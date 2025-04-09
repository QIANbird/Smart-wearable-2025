import pandas as pd
import matplotlib.pyplot as plt

# Load collected sensor data
df = pd.read_csv("sensor_data.csv")

# Convert time to seconds
df["Time"] = df["Time"].astype(float) / 1000  # Convert ms to seconds

# Plot each pressure sensor
plt.figure(figsize=(10, 6))
for i in range(1, 6):  # Assuming 5 insole sensors
    plt.plot(df["Time"], df[f"S{i}_Voltage"], label=f"Insole Sensor {i}")

plt.xlabel("Time (s)")
plt.ylabel("Pressure Sensor Voltage (V)")
plt.title("Pressure Sensor Readings Over Time")
plt.legend()
plt.show()


import numpy as np
import seaborn as sns

# Simulate a foot pressure heatmap (Example Data)
pressure_data = np.random.rand(3, 3)  # 3x3 matrix representing insole sensor grid

# Create heatmap
plt.figure(figsize=(5, 5))
sns.heatmap(pressure_data, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Foot Pressure Heatmap")
plt.xlabel("Toe → Heel")
plt.ylabel("Left → Right")
plt.show()
