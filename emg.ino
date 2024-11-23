#include <WiFi.h>

const char* ssid = "iPhone (7)";
const char* pass = "enes2003";

WiFiServer server(80);
String header;

const int analogPin = 34;
unsigned long currentTime = millis();
unsigned long clientPreviousTime = 0; 
const long timeoutTime = 2000;

unsigned long sensorPreviousTime = 0; 
const long sensorInterval = 1;

// Define a structure to hold sensor readings and timestamps
struct SensorData {
  unsigned long timestamp;
  int value;
};

// Define an array to store sensor data
const int maxDataPoints = 50; // Maximum number of data points to store
SensorData dataPoints[maxDataPoints];
int dataPointCount = 0;

void setup() {
  Serial.begin(115200);
  pinMode(analogPin, INPUT);
  WiFi.begin(ssid,pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  for (int a = 0;a <=200 ; a++){
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
    server.begin();
  }
}

void loop() {
  handleClient();
  readAndSendSensorData();
}

void handleClient() {
  WiFiClient client = server.available();
  if (client) {
    currentTime = millis();
    clientPreviousTime = currentTime;
    Serial.println("New Client.");
    String currentLine = "";
    while (client.connected() && currentTime - clientPreviousTime <= timeoutTime) {
      currentTime = millis();
      if (client.available()) {
        char c = client.read();
        Serial.write(c);
        header += c;
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            client.println("<!DOCTYPE html><html><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><link rel=\"icon\" href=\"data:,\">");
            client.println("<meta http-equiv=\"refresh\" content=\"3\"><title>ESP32 Analog Sensor</title></head><body><h1>Analog Sensor Value</h1>");
            
            // Display sensor data with timestamps
            client.println("<p>Sensor Readings:</p>");
            client.println("<ul>");
            for (int i = 0; i < dataPointCount; i++) {
              client.print("<li>");
              client.print("Timestamp: ");
              client.print(dataPoints[i].timestamp);
              client.print(", Value: ");
              client.print(dataPoints[i].value);
              client.println("</li>");
            }
            client.println("</ul>");
            
            client.println("</body></html>");
            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = "";
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}

void readAndSendSensorData() {
  // Read sensor data and store it with timestamps
  unsigned long currentMillis = millis();
  if (currentMillis - sensorPreviousTime >= sensorInterval) { // Update every 1 millisecond
    int sensorValue = analogRead(analogPin);
    Serial.print("Sensor value: ");
    Serial.println(sensorValue);
    // Store sensor data with timestamp
    SensorData newData;
    newData.timestamp = currentMillis;
    newData.value = sensorValue;
    // Add data to array
    if (dataPointCount < maxDataPoints) {
      dataPoints[dataPointCount] = newData;
      dataPointCount++;
    }
    else {
      // If array is full, shift elements and add new data at the end
      for (int i = 0; i < maxDataPoints - 1; i++) {
        dataPoints[i] = dataPoints[i + 1];
      }
      dataPoints[maxDataPoints - 1] = newData;
    }
    sensorPreviousTime = currentMillis;
  }
}
