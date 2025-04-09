#include <WiFiNINA.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "martix";
const char* password = "lovejudo99";

// Google Colab ngrok URL (HTTPS)
const char* serverIP = "c9ef-34-150-208-138.ngrok-free.app";  
const int serverPort = 443;  // Use 443 for HTTPS

WiFiSSLClient client;  // 🔹 Use WiFiSSLClient for HTTPS

// Sensor setup
const int sensorPins[6] = {A0, A1, A2, A3, A4, A5};  
const float fixedResistors[6] = {820.0, 820.0, 820.0, 820.0, 820.0, 820.0};  
const float VCC = 3.3;  
const int samplingRate = 20;  // 50Hz

void setup() {
    Serial.begin(115200);

    // Connect to WiFi
    Serial.print("Connecting to WiFi...");
    while (WiFi.begin(ssid, password) != WL_CONNECTED) { 
        Serial.print("."); 
        delay(1000);
    }
    Serial.println(" Connected!");

    Serial.print("Connecting to server...");
    if (client.connect(serverIP, serverPort)) {  // 🔹 Now uses HTTPS (port 443)
        Serial.println("Connected to Python Server!");
    } else { 
        Serial.println("Connection to server FAILED!");
    }
}

void sendData() {
    if (client.connect(serverIP, serverPort)) {  // 🔹 Use HTTPS
        StaticJsonDocument<256> jsonDoc;
        jsonDoc["timestamp"] = millis();

        JsonArray voltageArray = jsonDoc.createNestedArray("voltages");
        JsonArray resistanceArray = jsonDoc.createNestedArray("resistances");

        for (int i = 0; i < 6; i++) {
            int sensorValue = analogRead(sensorPins[i]);  
            float voltage = (sensorValue / 1023.0) * VCC;
            voltageArray.add(voltage);

            float resistance = (voltage > 0 && voltage < VCC) ? 
                (fixedResistors[i] * (voltage / (VCC - voltage))) : -1;
            resistanceArray.add(resistance);
        }

        // Convert JSON to string
        String jsonString;
        serializeJson(jsonDoc, jsonString);

        // Send HTTP POST request
        client.println("POST /data HTTP/1.1");
        client.println("Host: " + String(serverIP));
        client.println("Content-Type: application/json");
        client.print("Content-Length: ");
        client.println(jsonString.length());
        client.println();
        client.println(jsonString);
        
        Serial.println("Sent: " + jsonString);

        delay(500);  // Wait for response
        while (client.available()) {
            char c = client.read();
            Serial.write(c);  // Print server response
        }
        
        client.stop();
    } else {
        Serial.println("Connection to server failed!");
    }
}

void loop() {
    sendData();
    delay(samplingRate);
}
