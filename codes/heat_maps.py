import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import griddata

# List of files to process
file_paths = [
    "standing_15s.csv",
    "standing_foot_eversion_15s.csv",
    "side_foot_15s.csv",
    "toes_15s.csv",
    "heel_15s.csv"
]

# Custom titles for each file
custom_titles = {
    "standing_15s.csv": "Standing Position",
    "standing_foot_eversion_15s.csv": "Standing with Foot Eversion",
    "side_foot_15s.csv": "Side of Foot Pressure",
    "toes_15s.csv": "Heel Pressure",
    "heel_15s.csv": "Toe Pressure"
}

fs = 100  # Sampling frequency in Hz
dt = 1 / fs  # Time step

# Create a figure with subplots
fig, axes = plt.subplots(1, len(file_paths), figsize=(15, 6))

# Sensor positions for a triangular shape
sensor_positions = np.array([
    [1, 0],    # Heel (bottom)
    [0.5, 1.5], # Midfoot (middle)
    [1.5, 3]   # Toes (top)
])

for i, file_path in enumerate(file_paths):
    try:
        # Load the data
        df = pd.read_csv(file_path)

        # Extract sensor data (assuming sensors are in columns 7, 8, and 9)
        if df.shape[1] >= 10:
            sensor1 = df.iloc[:, 9].values  # Heel
            sensor2 = df.iloc[:, 8].values  # Midfoot
            sensor3 = df.iloc[:, 7].values  # Toes
        else:
            raise ValueError("The file does not have at least 10 columns.")

        # Compute mean pressures
        sensor_pressures = np.array([
            np.mean(sensor1),
            np.mean(sensor2),
            np.mean(sensor3)
        ])

        # Ensure no NaN values
        sensor_pressures = np.nan_to_num(sensor_pressures, nan=np.nanmean(sensor_pressures))

        # Generate grid within the triangular area
        grid_x, grid_y = np.meshgrid(np.linspace(0, 2, 50), np.linspace(0, 3, 50))

        # Interpolate pressure values over the grid
        grid_pressures = griddata(sensor_positions, sensor_pressures / 1000, (grid_x, grid_y), method='linear')

        # Mask to keep only the triangular area
        mask = (grid_y >= (grid_x * 1.5 - 1.5)) & (grid_y >= (-grid_x * 1.5 + 3))
        grid_pressures[~mask] = np.nan  # Remove values outside the triangle

        # Plot triangular heatmap
        sns.heatmap(grid_pressures, cmap="coolwarm", cbar=True, xticklabels=False, yticklabels=False, ax=axes[i])
        axes[i].set_title(custom_titles.get(file_path, "Unknown"))  # Use custom title or "Unknown" if not in dict
        axes[i].set_xlabel("Foot Width")
        axes[i].set_ylabel("Foot Length")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

plt.tight_layout()
plt.show()
