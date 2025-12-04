#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <DHT.h>

// ----- WiFi & Firebase Config -----
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Your Firebase Database Host (without https://)
const char* FIREBASE_HOST = "your-project-id-default-rtdb.firebaseio.com";
const char* FIREBASE_AUTH = ""; // Add database secret if rules are locked

// ----- Hardware Pins -----
#define DHTPIN 4        // D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const uint8_t IR_IN_PIN  = 14; // D5
const uint8_t IR_OUT_PIN = 12; // D6
const uint8_t LED_PIN    = 13; // D7
const uint8_t MOTOR_PIN  = 15; // D8
const uint8_t LDR_PIN    = A0;

// ----- Constants -----
const int LDR_DARK_THRESHOLD = 500;
const float TEMP_MOTOR_ON    = 30.0;
const int PEOPLE_MOTOR_ON    = 6;
const unsigned long IR_DEBOUNCE_MS = 120UL;

// ----- Variables -----
volatile bool irInFlag = false;
volatile bool irOutFlag = false;
volatile unsigned long lastIrInTime = 0;
volatile unsigned long lastIrOutTime = 0;
int people = 0;

float ldrEMA = -1.0f; 
const float LDR_ALPHA = 0.12f;

float lastTemp = 0.0;
float lastHum = 0.0;

// ----- Control State (Fetched from Cloud) -----
bool ledManual = false;
bool ledState = false;
bool ledStop = false;
bool motorManual = false;
bool motorState = false;
bool motorStop = false;

WiFiClientSecure client;

// ---------------- ISRs ----------------
ICACHE_RAM_ATTR void IRInISR()  { irInFlag = true; }
ICACHE_RAM_ATTR void IROutISR() { irOutFlag = true; }

// ---------------- Helpers ----------------
int calculateAutoMotorPWM(float temp, int peopleCount) {
  int p1 = 0;
  if (!isnan(temp) && temp > TEMP_MOTOR_ON) {
    p1 = constrain((int)((temp - TEMP_MOTOR_ON) * 12), 0, 255);
  }
  int p2 = 0;
  if (peopleCount >= PEOPLE_MOTOR_ON) {
    p2 = map(min(peopleCount, 20), PEOPLE_MOTOR_ON, 20, 80, 255);
  }
  return max(p1, p2);
}

int calculateAutoLedPWM(int ldrRaw, int peopleCount) {
  float darkFactor = (ldrRaw <= LDR_DARK_THRESHOLD) ? 1.0f : constrain(1.0f - (float)(ldrRaw - LDR_DARK_THRESHOLD)/200.0f, 0.0f, 1.0f);
  float peopleFactor = constrain((float)peopleCount/8.0f, 0.0f, 1.0f);
  float combined = (darkFactor > peopleFactor*0.6) ? darkFactor : peopleFactor*0.6;
  return (int)(combined*255.0);
}

// ---------------- Network Functions ----------------
void ensureWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.print("WiFi Disconnected. Reconnecting");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected.");
  client.setInsecure(); // Important for Firebase HTTPS
}

// Simple JSON parser for boolean fields to avoid heavy libraries
// Looks for "key":true or "key":false
bool parseBool(String json, String key) {
  int keyIndex = json.indexOf(key);
  if (keyIndex == -1) return false; // Default safe
  
  // Look ahead for "true" or "false"
  int trueIndex = json.indexOf("true", keyIndex);
  int falseIndex = json.indexOf("false", keyIndex);
  
  // Check which one comes first after the key
  if (trueIndex != -1 && (falseIndex == -1 || trueIndex < falseIndex)) {
     // Verify it's actually the value for this key (roughly)
     if (trueIndex - keyIndex < 20) return true;
  }
  return false;
}

void fetchControls() {
  if (!client.connect(FIREBASE_HOST, 443)) return;

  String url = "/control.json";
  if (String(FIREBASE_AUTH).length() > 0) url += "?auth=" + String(FIREBASE_AUTH);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + FIREBASE_HOST + "\r\n" +
               "Connection: close\r\n\r\n");

  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") break;
  }
  
  String body = client.readString();
  
  // Parse manually (e.g. {"ledManual":true,...})
  ledManual = parseBool(body, "\"ledManual\"");
  ledState = parseBool(body, "\"ledState\"");
  ledStop = parseBool(body, "\"ledStop\"");
  
  motorManual = parseBool(body, "\"motorManual\"");
  motorState = parseBool(body, "\"motorState\"");
  motorStop = parseBool(body, "\"motorStop\"");
  
  Serial.println("Controls Fetched.");
}

void uploadStatus(int finalLedPWM, int finalMotorPWM, int ldrVal) {
  if (!client.connect(FIREBASE_HOST, 443)) return;

  // Build JSON manually
  String json = "{";
  json += "\"temp\":" + String(lastTemp) + ",";
  json += "\"hum\":" + String(lastHum) + ",";
  json += "\"people\":" + String(people) + ",";
  json += "\"ldr\":" + String(ldrVal) + ",";
  json += "\"ledPWM\":" + String(finalLedPWM) + ",";
  json += "\"motorPWM\":" + String(finalMotorPWM);
  json += "}";

  String url = "/status.json";
  if (String(FIREBASE_AUTH).length() > 0) url += "?auth=" + String(FIREBASE_AUTH);

  client.print(String("PUT ") + url + " HTTP/1.1\r\n" +
               "Host: " + FIREBASE_HOST + "\r\n" +
               "Content-Type: application/json\r\n" +
               "Content-Length: " + json.length() + "\r\n" +
               "Connection: close\r\n\r\n" +
               json);
               
  // Flush response
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (line == "\r") break;
  }
  while (client.available()) client.read();
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(115200);
  dht.begin();
  
  pinMode(IR_IN_PIN, INPUT);
  pinMode(IR_OUT_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LDR_PIN, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(IR_IN_PIN), IRInISR, FALLING);
  attachInterrupt(digitalPinToInterrupt(IR_OUT_PIN), IROutISR, FALLING);
  
  analogWriteRange(255);

  ensureWiFi();
}

// ---------------- Loop ----------------
unsigned long lastCloudUpdate = 0;

void loop() {
  ensureWiFi();
  unsigned long now = millis();

  // 1. Process IR Sensors (Immediate)
  if(irInFlag){
    irInFlag = false;
    if(now - lastIrInTime > IR_DEBOUNCE_MS && now - lastIrOutTime > 20){
      people++;
      lastIrInTime = now;
    }
  }
  if(irOutFlag){
    irOutFlag = false;
    if(now - lastIrOutTime > IR_DEBOUNCE_MS && now - lastIrInTime > 20){
      if(people > 0) people--;
      lastIrOutTime = now;
    }
  }

  // 2. Read Sensors (Continuous smoothing)
  int ldrRaw = analogRead(LDR_PIN);
  if(ldrEMA < 0) ldrEMA = ldrRaw;
  else ldrEMA = LDR_ALPHA*ldrRaw + (1-LDR_ALPHA)*ldrEMA;

  // 3. Cloud Sync Cycle (Every 2 seconds)
  if (now - lastCloudUpdate > 2000) {
    lastCloudUpdate = now;

    // A. Read Temp/Hum
    float t = dht.readTemperature();
    float h = dht.readHumidity();
    if(!isnan(t)) lastTemp = t;
    if(!isnan(h)) lastHum = h;

    // B. Get Controls from Firebase
    fetchControls();

    // C. Calculate Outputs
    int targetLedPWM = 0;
    if (ledStop) {
        targetLedPWM = 0;
    } else if (ledManual) {
        targetLedPWM = ledState ? 255 : 0;
    } else {
        targetLedPWM = calculateAutoLedPWM((int)round(ldrEMA), people);
    }

    int targetMotorPWM = 0;
    if (motorStop) {
        targetMotorPWM = 0;
    } else if (motorManual) {
        targetMotorPWM = motorState ? 255 : 0;
    } else {
        targetMotorPWM = calculateAutoMotorPWM(lastTemp, people);
    }

    // D. Actuate
    analogWrite(LED_PIN, targetLedPWM);
    analogWrite(MOTOR_PIN, targetMotorPWM);

    // E. Upload Status to Firebase
    uploadStatus(targetLedPWM, targetMotorPWM, (int)round(ldrEMA));
    
    Serial.print("P:"); Serial.print(people);
    Serial.print(" T:"); Serial.print(lastTemp);
    Serial.print(" LED:"); Serial.print(targetLedPWM);
    Serial.print(" MTR:"); Serial.println(targetMotorPWM);
  }
}