#include <Wire.h>
#include <Adafruit_BMP280.h>
#include "DHT.h"

// ----------- Pins -----------
#define DHTPIN 2
#define DHTTYPE DHT11
#define RAIN_DIGITAL_PIN 5  // D5
#define RAIN_ANALOG_PIN A0  // A0
#define LDR_PIN A1
#define LDR_THRESHOLD 500   // Digital threshold for LDR

// ----------- Sensors -----------
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;  // I2C

// ----------- Data struct -----------
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

// ----------- Timing -----------
unsigned long previousMillis = 0;
const unsigned long interval = 30000; // 30 seconds

// ----------- Function to read and send all data -----------
void readAndSendData() {
  // --- Read DHT11 ---
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (isnan(t) || isnan(h)) { t = 0; h = 0; }

  // --- Read BMP280 ---
  float bmpTemp = bmp.readTemperature();
  float bmpPressure = bmp.readPressure() / 100.0; // hPa
  float bmpAlt = bmp.readAltitude(1013.25);

  // --- Rain sensor ---
  int rainDigital = digitalRead(RAIN_DIGITAL_PIN);
  int rainAnalog = analogRead(RAIN_ANALOG_PIN);

  // --- LDR ---
  int ldrRaw = analogRead(LDR_PIN);
  int ldrDigital = (ldrRaw > LDR_THRESHOLD) ? HIGH : LOW;
  float ldrPct = (ldrRaw / 1023.0) * 100.0;

  // --- Save to struct ---
  latestData = {t, h, bmpTemp, bmpPressure, bmpAlt, rainDigital, rainAnalog, ldrDigital, ldrRaw, ldrPct};

  // --- SEND DATA PACKET ---
  Serial.print("<"); 
  Serial.print(latestData.dhtTemp); Serial.print(",");
  Serial.print(latestData.dhtHumi); Serial.print(",");
  Serial.print(latestData.bmpTemp); Serial.print(",");
  Serial.print(latestData.bmpPressure); Serial.print(",");
  Serial.print(latestData.bmpAlt); Serial.print(",");
  Serial.print(latestData.rainDigital); Serial.print(",");
  Serial.print(latestData.rainAnalog); Serial.print(",");
  Serial.print(latestData.ldrDigital); Serial.print(",");
  Serial.print(latestData.ldrRaw); Serial.print(",");
  Serial.print(latestData.ldrPct);
  Serial.println(">");
}

void setup() {
  Serial.begin(9600);
  dht.begin();

  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 not detected!");
  }

  pinMode(RAIN_DIGITAL_PIN, INPUT);

  // 🔥🔥 IMMEDIATE FIRST SENSOR READ
  readAndSendData();

  // Set timer starting point
  previousMillis = millis();
}

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Regular 30-second interval read
    readAndSendData();
  }
}
