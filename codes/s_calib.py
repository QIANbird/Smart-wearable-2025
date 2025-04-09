import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
import seaborn as sns

# Define sensors, file paths, and sensor-specific areas
sensors = {
    "s1": (0.00004, 7),  # Sensor s1: area and column index (zero-based, 8th column)
    "s2": (0.00005, 8),  # Sensor s2: area and column index (9th column)
    "s3": (0.00016, 9),  # Sensor s3: area and column index (10th column)
    "s4": (0.00019, 10), # Sensor s4: area and column index (11th column)
    "s5": (0.00019, 11), # Sensor s5: area and column index (12th column)
    "s6": (0.00019, 12)  # Sensor s6: area and column index (13th column)
}
pressures = [0, 200, 500, 700]  # Mass in grams
g = 9.81  # Gravitational acceleration (m/s²)

# Initialize storage for results
sensor_results = {sensor: {"pressures": [], "mean_resistances": [], "std_resistances": []} for sensor in sensors}

for sensor, (sensor_area, column_index) in sensors.items():
    for mass in pressures:
        file_name = f"{sensor}_{mass}g.csv"  # Each sensor has its own file
        try:
            # Load the data
            df = pd.read_csv(file_name)
            
            # Extract the corresponding column of resistance values
            resistance_values = df.iloc[:, column_index]  # Use correct column index per sensor
            
            # Compute mean and standard deviation
            mean_resistance = resistance_values.mean()
            std_resistance = resistance_values.std()
            
            # Convert mass to pressure (P = mg/A)
            pressure = (mass / 1000 * g) / sensor_area  # Pressure in Pascals (Pa)
            
            # Store results
            sensor_results[sensor]["pressures"].append(pressure / 1000)
            sensor_results[sensor]["mean_resistances"].append(mean_resistance / 1000)
            sensor_results[sensor]["std_resistances"].append(std_resistance / 1000)
            
            print(f"Processed {file_name} for {sensor}: Mass={mass}g, Pressure={pressure:.2f} Pa, Mean Resistance={mean_resistance:.2f}, Std={std_resistance:.2f}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# Plot Pressure vs. Resistance curves for each sensor
plt.figure(figsize=(8,6))
for sensor in sensors.keys():
    plt.errorbar(sensor_results[sensor]["pressures"], sensor_results[sensor]["mean_resistances"],
                 yerr=sensor_results[sensor]["std_resistances"], fmt='o-', capsize=5, label=f'{sensor} Mean ± Std Dev')

plt.xlabel("Pressure [kPa]")
plt.ylabel("Resistance [kOhm]")
plt.title("Pressure vs. Resistance Curves for Multiple Sensors")
plt.legend()
plt.grid(True)
plt.show()

##########################

# Define higher pressures for extrapolation
higher_pressures = np.linspace(0, 500, 20)  # Extend up to 3x current max

plt.figure(figsize=(8,6))

for sensor in sensors.keys():
    # Extract actual data
    P_actual = np.array(sensor_results[sensor]["pressures"])
    R_actual = np.array(sensor_results[sensor]["mean_resistances"])
    std_R_actual = np.array(sensor_results[sensor]["std_resistances"])  # Standard deviation

    # Debugging: Print raw values
    print(f"\nSensor: {sensor}")
    print(f"Raw Pressures: {P_actual}")
    print(f"Raw Resistances: {R_actual}")

    # Remove zero-pressure values to avoid log(0)
    valid_indices = (P_actual > 0) & (R_actual > 0)  # Ensure both pressure and resistance are non-zero
    P_actual = P_actual[valid_indices]
    R_actual = R_actual[valid_indices]
    std_R_actual = std_R_actual[valid_indices]  # Filter std deviations as well

    # Debugging: Print filtered values
    print(f"Filtered Pressures: {P_actual}")
    print(f"Filtered Resistances: {R_actual}")

    # Skip sensor if no valid data remains
    if len(P_actual) < 2:
        print(f"Skipping {sensor} due to insufficient valid data")
        continue

    # Transform data to log-log space for better numerical stability
    log_P = np.log(P_actual)
    log_R = np.log(R_actual)

    # Debugging: Print log values
    print(f"log_P: {log_P}")
    print(f"log_R: {log_R}")

    # Linear fit in log-log space (equivalent to power law fit)
    try:
        slope, intercept = np.polyfit(log_P, log_R, 1)
        k_fit = np.exp(intercept)  # Convert back from log-space
        n_fit = -slope  # Convert slope to power law exponent

        # Debugging: Print fitted parameters
        print(f"Fitted Parameters - k: {k_fit}, n: {n_fit}")

        # Predict resistances for higher pressures
        R_predicted = k_fit * higher_pressures**-n_fit

        # Plot actual and extrapolated data
        #plt.errorbar(P_actual, R_actual, yerr=std_R_actual, fmt='o-', label=f'{sensor} Actual')  # Fixed size mismatch
        plt.plot(higher_pressures, R_predicted, label=f'{sensor} Extrapolated', linewidth=2.5)

    except Exception as e:
        print(f"Curve fitting failed for {sensor}: {e}")

plt.xlabel("Pressure [kPa]")
plt.ylabel("Resistance [kOhms]")
plt.title("Extrapolated Pressure vs. Resistance Curves")
plt.legend()
plt.grid(True)
plt.show()

############ SENSITIVITY CALCULATION ################

# Compute slope in linear range
for sensor in sensors.keys():
    P_actual = np.array(sensor_results[sensor]["pressures"])
    R_actual = np.array(sensor_results[sensor]["mean_resistances"])

    # Use only a linear range (e.g., first 50% of values)
    linear_range = int(len(P_actual) * 0.5)
    slope, _ = np.polyfit(P_actual[:linear_range], R_actual[:linear_range], 1)

    print(f"Sensor {sensor}: Sensitivity = {slope:.4f} kOhm/kPa")
    
############ RISE/FALL TIME ##############
# Load the data
file_path = "response_time_s1.csv"
df = pd.read_csv(file_path)

# Sampling frequency
fs = 100  # Hz
dt = 1 / fs  # Time step

# Extract the 8th column (index 7 in zero-based indexing)
if df.shape[1] >= 8:
    signal = df.iloc[:, 7].values
else:
    raise ValueError("The file does not have at least 8 columns.")

# Create time vector
time = np.arange(len(signal)) * dt

# Plot the signal
plt.figure(figsize=(8, 6))
plt.plot(time, signal, label="Rise time test with weight", color=sns.color_palette("muted")[0])
plt.xlabel("Time [s]")
plt.ylabel("Resistance [kOhms]")
plt.title("Resistance of piezoresistive sensor")
plt.grid(True)
plt.show()

# Detect time rise (simple threshold-based approach)
threshold = 0.35 * (np.max(signal) - np.min(signal)) + np.min(signal)  # % rise
rise_time_index = np.where(signal >= threshold)[0][0]  # First index above threshold
rise_time = rise_time_index * dt  # Convert index to time

print(f"Estimated rise time: {rise_time:.4f} seconds")