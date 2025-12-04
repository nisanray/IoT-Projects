#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <time.h> // Required for structure tm

// --------- WIFI CONFIGURATION (UPDATE THESE) ----------
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// --------- FIREBASE CONFIGURATION (UPDATE THESE) ----------
const char* FIREBASE_HOST = "your-project-id-default-rtdb.firebaseio.com"; 
const char* FIREBASE_AUTH = ""; // Leave empty if your rules are public, otherwise add secret

// --------- NTP SETUP ----------
WiFiUDP ntpUDP;
// Offset for GMT+6 (Bangladesh) is 21600 seconds. Change if needed.
const long utcOffsetInSeconds = 21600;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds, 60000);

// --------- HTTPS CLIENT ----------
WiFiClientSecure client;

// --------- FUNCTIONS ----------

void ensureWiFiConnected() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("\nWiFi Reconnected");
  }
}

// Helper to generate format: 2025-12-04T01-15-30+06-00
String getCustomTimestamp() {
  time_t rawTime = timeClient.getEpochTime();
  struct tm * timeinfo = gmtime(&rawTime);
  
  char buffer[35];
  sprintf(buffer, "%04d-%02d-%02dT%02d-%02d-%02d+06-00", 
          timeinfo->tm_year + 1900, 
          timeinfo->tm_mon + 1, 
          timeinfo->tm_mday, 
          timeinfo->tm_hour, 
          timeinfo->tm_min, 
          timeinfo->tm_sec);
          
  return String(buffer);
}

void uploadHelloWorld() {
  if (WiFi.status() != WL_CONNECTED) return;

  // 1. Create the unique key based on time
  String key = getCustomTimestamp();
  
  // 2. Define the path in the database
  String url = "/readings/" + key + ".json";
  
  // Add Auth token if provided
  if (strlen(FIREBASE_AUTH) > 0) {
    url += "?auth=" + String(FIREBASE_AUTH);
  }

  // 3. Create the JSON Payload
  // This sends: {"message": "Hello World"}
  String json = "{\"message\": \"Hello World\"}";

  client.setInsecure(); // Required for HTTPS without certificate validation

  Serial.print("Connecting to Firebase... ");
  if (!client.connect(FIREBASE_HOST, 443)) {
    Serial.println("Connection failed!");
    return;
  }
  Serial.println("Connected.");

  // 4. Construct HTTP PUT Request
  String req =
    "PUT " + url + " HTTP/1.1\r\n" +
    "Host: " + FIREBASE_HOST + "\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: " + json.length() + "\r\n" +
    "Connection: close\r\n\r\n" +
    json;

  client.print(req);
  
  // 5. Read Response (Optional, but good for debugging)
  while(client.connected()) {
    String line = client.readStringUntil('\n');
    if(line == "\r") break; // Headers finished
  }
  // Flush remaining
  while(client.available()) client.read();
  
  Serial.print("Success! Uploaded 'Hello World' at: ");
  Serial.println(key);
}

// --------- MAIN SETUP ----------

void setup() {
  Serial.begin(115200);   
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  Serial.println("\nConnecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); 
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");

  timeClient.begin();
  client.setInsecure();
}

// --------- MAIN LOOP ----------

void loop() {
  ensureWiFiConnected();
  timeClient.update();
  
  // Upload "Hello World"
  uploadHelloWorld();
  
  // Wait 10 seconds before sending again
  delay(10000); 
}