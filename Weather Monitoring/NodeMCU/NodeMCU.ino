#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <SoftwareSerial.h>
#include <time.h> // Required for structure tm

// --------- WIFI ----------
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// --------- FIREBASE ----------
const char* FIREBASE_HOST = "your-project-id-default-rtdb.firebaseio.com"; 
const char* FIREBASE_AUTH = ""; 

// --------- SERIAL CONFIG ----------
SoftwareSerial UNO_SERIAL(5, 4); // D1, D2

// --------- NTP ----------
WiFiUDP ntpUDP;
// Offset for GMT+6 (Bangladesh) is 21600 seconds (6 * 3600)
const long utcOffsetInSeconds = 21600;
NTPClient timeClient(ntpUDP, "pool.ntp.org", utcOffsetInSeconds, 60000);

// --------- HTTPS ----------
WiFiClientSecure client;

// --------- Data ----------
struct SensorData {
  float dhtTemp;
  float dhtHumi;
  float bmpTemp;
  float bmpPressure;
  float bmpAlt;
  int rainDigital;
  int rainAnalog;
  int ldrDigital;
  int ldrRaw;
  float ldrPct;
};
SensorData latestData;

// --------- FUNCTIONS ----------

void ensureWiFiConnected() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    WiFi.begin(ssid, password);
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

String sensorDataToJSON() {
  String json = "{";
  json += "\"ts\":" + String(timeClient.getEpochTime()) + ",";
  json += "\"dht_temp\":" + String(latestData.dhtTemp,2) + ",";
  json += "\"dht_humi\":" + String(latestData.dhtHumi,2) + ",";
  json += "\"bmp_temp\":" + String(latestData.bmpTemp,2) + ",";
  json += "\"bmp_pres\":" + String(latestData.bmpPressure,2) + ",";
  json += "\"bmp_alt\":" + String(latestData.bmpAlt,2) + ",";
  json += "\"rain_digital\":" + String(latestData.rainDigital) + ",";
  json += "\"rain_analog\":" + String(latestData.rainAnalog) + ",";
  json += "\"ldr_digital\":" + String(latestData.ldrDigital) + ",";
  json += "\"ldr_raw\":" + String(latestData.ldrRaw) + ",";
  json += "\"ldr_pct\":" + String(latestData.ldrPct,1);
  json += "}";
  return json;
}

void uploadISO(String json) {
  if (WiFi.status() != WL_CONNECTED) return;

  // Generate the formatted ID
  String key = getCustomTimestamp();
  String url = "/readings/" + key + ".json";
  
  if (strlen(FIREBASE_AUTH) > 0) url += "?auth=" + String(FIREBASE_AUTH);

  client.setInsecure(); 

  if (!client.connect(FIREBASE_HOST, 443)) {
    Serial.println("Firebase connection failed");
    return;
  }

  String req =
    "PUT " + url + " HTTP/1.1\r\n" +
    "Host: " + FIREBASE_HOST + "\r\n" +
    "Content-Type: application/json\r\n" +
    "Content-Length: " + json.length() + "\r\n" +
    "Connection: close\r\n\r\n" +
    json;

  client.print(req);
  
  // Wait for response
  while(client.connected()) {
    String line = client.readStringUntil('\n');
    if(line == "\r") break;
  }
  
  Serial.print("Data uploaded: ");
  Serial.println(key);
}

void readFromUnoAndUpload() {
  // Check if data is coming from Arduino
  while (UNO_SERIAL.available() > 0) {
    String line = UNO_SERIAL.readStringUntil('>');
    int startIdx = line.indexOf('<');
    if (startIdx == -1) return; 

    String clean = line.substring(startIdx + 1);
    clean.trim();

    Serial.println("Received: " + clean);

    float values[10];
    int from = 0;
    bool error = false;
    
    for (int i = 0; i < 10; i++) {
      int comma = clean.indexOf(',', from);
      if (i < 9 && comma == -1) { error = true; break; }
      
      if (i == 9) values[i] = clean.substring(from).toFloat();
      else values[i] = clean.substring(from, comma).toFloat();
      
      from = comma + 1;
    }

    if (!error) {
      // 1. Update Data Structure
      latestData = {
        values[0], values[1], values[2], values[3], values[4],
        (int)values[5], (int)values[6], (int)values[7], (int)values[8], values[9]
      };

      // 2. Upload IMMEDIATELY (No waiting for timer)
      String json = sensorDataToJSON();
      uploadISO(json);
    }
  }
}

void setup() {
  Serial.begin(115200);   
  UNO_SERIAL.begin(9600); 

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); Serial.print(".");
  }
  Serial.println("\nWiFi Connected");

  timeClient.begin();
  client.setInsecure();
}

void loop() {
  ensureWiFiConnected();
  timeClient.update();
  
  // This function now handles reading AND uploading instantly
  readFromUnoAndUpload();
}