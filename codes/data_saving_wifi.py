import socket
import json
import csv

# Server settings
HOST = "0.0.0.0"  # Listen on all network interfaces (change to PC IP if needed)
PORT = 5001  # Must match Arduino's port

# CSV setup
CSV_FILE = "wifi_sensor_data.csv"

# Open CSV file for writing
with open(CSV_FILE, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Header for CSV file
    csv_writer.writerow(["Timestamp (ms)", "S1_Voltage", "S2_Voltage", "S3_Voltage", "S4_Voltage", "S5_Voltage", "S6_Voltage",
                        "S1_Resistance", "S2_Resistance", "S3_Resistance", "S4_Resistance", "S5_Resistance", "S6_Resistance"])

    # Start TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Listening for Arduino connections on port {PORT}...")

        conn, addr = server.accept()
        print(f"Connected to {addr}")

        try:
            while True:
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    continue

                try:
                    json_data = json.loads(data)  # Parse JSON from Arduino
                    time_stamp = json_data["timestamp"]  # Use correct timestamp field
                    voltages = json_data["voltages"]
                    resistances = json_data["resistances"]

                    # Ensure proper formatting
                    if len(voltages) == 6 and len(resistances) == 6:
                        csv_writer.writerow([time_stamp] + voltages + resistances)
                        print(f"Saved: {time_stamp}, Voltages: {voltages}, Resistances: {resistances}")
                    else:
                        print("Received incorrect data format, skipping...")

                except json.JSONDecodeError:
                    print("Invalid JSON received, skipping...")

        except KeyboardInterrupt:
            print("\nStopping server...")
            conn.close()
