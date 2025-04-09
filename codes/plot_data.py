import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of files to process
file_paths = [
    "E:\Aalto\smart wearable\codes\Data_Collected\zeroCalibration_Xie_02.csv"
    "standing_15s.csv",
    "standing_foot_eversion_15s.csv",
    "side_foot_15s.csv",
    "toes_15s.csv",
    "heel_15s.csv",
    "walk_id1.csv",
    "walk_everted.csv",
    "walk_id2.csv",
    "walk_id2_evertion.csv"
]

fs = 100  # Sampling frequency in Hz
dt = 1 / fs  # Time step

for file_path in file_paths:
    try:
        # Load the data
        df = pd.read_csv(file_path)
        
        # Extract sensor data from 8th column onward
        sensor_data = df.iloc[:, 7:]
        
        # Compute standard deviations
        std_devs = sensor_data.std()
        print(f"Standard deviations for {file_path}:")
        print(std_devs)
        print("-" * 50)
        
        # Create time vector
        time = np.arange(len(sensor_data)) * dt
        
        # Define custom legend labels
        legend_labels = [f"Sensor {i+1}" for i in range(sensor_data.shape[1])]
        
        # Plot each sensor's signal
        plt.figure(figsize=(10, 6))
        for col, label in zip(sensor_data.columns, legend_labels):
            plt.plot(time, sensor_data[col]/1000, label=label)
        
        plt.xlabel("Time [s]")
        plt.ylabel("Resistance [kOhm]")
        plt.title(f"Sensor Data for {file_path}")
        plt.legend(loc="upper right")  # Add legend with custom labels
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
