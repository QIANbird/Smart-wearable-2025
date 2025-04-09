#include <ArduinoJson.h>

const int sensorPins[6] = {A0, A1, A2, A3, A4, A5};  
const float fixedResistors[6] = {820.0, 820.0, 820.0, 820.0, 820.0, 820.0};  
const float VCC = 3.3;  

void setup() {
    Serial.begin(115200);  // Faster baud rate for Python communication
    while (!Serial);  // Wait for Serial connection
}

void loop() {
    StaticJsonDocument<256> jsonDoc; // JSON object to store data

    jsonDoc["time"] = millis(); // Timestamp

    JsonArray voltageArray = jsonDoc.createNestedArray("voltages");
    JsonArray resistanceArray = jsonDoc.createNestedArray("resistances");

    for (int i = 0; i < 6; i++) {
        int sensorValue = analogRead(sensorPins[i]);  
        Serial.print(sensorValue);
        Serial.print(" ");
        float voltage = (sensorValue / 1023.0) * VCC;
        voltageArray.add(voltage);

        // Calculate resistance using voltage divider formula
        float resistance;
        if (voltage > 0 && voltage < VCC) {
            resistance = fixedResistors[i] * (voltage / (VCC - voltage));
        } else {
            resistance = -1; // Error indicator
        }
        resistanceArray.add(resistance);
    }

    // Serialize JSON and send over Serial
    //serializeJson(jsonDoc, Serial);
    Serial.println(); // Ensure Python reads complete JSON object
    delay(10);
}
