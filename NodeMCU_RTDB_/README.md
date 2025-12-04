# NodeMCU Firebase RTDB Template

![Project Type](https://img.shields.io/badge/Type-IoT%20Template-blue)
![Platform](https://img.shields.io/badge/Platform-ESP8266-green)
![Database](https://img.shields.io/badge/Database-Firebase%20RTDB-orange)

## 📋 Overview

A foundational template project demonstrating real-time data synchronization between NodeMCU (ESP8266) and Firebase Realtime Database. This project serves as a starting point for IoT applications requiring cloud connectivity with timestamp-based data logging.

## ✨ Features

- ✅ WiFi connectivity with auto-reconnection
- ✅ Firebase Realtime Database integration
- ✅ NTP time synchronization (GMT+6)
- ✅ Custom timestamp format for data organization
- ✅ Secure HTTPS communication
- ✅ Lightweight implementation without heavy libraries

## 🔧 Hardware Requirements

### Components
- **NodeMCU ESP8266** (1x)
- **Micro USB Cable** (for programming and power)

### Pin Configuration

| Component | NodeMCU Pin | GPIO | Function |
|-----------|-------------|------|----------|
| USB Power | VU/5V | - | Power Supply (5V) |
| Ground | GND | - | Ground Reference |

**Note:** This is a template project with no external sensors. It demonstrates the basic Firebase connectivity framework.

## 📊 Circuit Diagram

```
┌─────────────────────┐
│   NodeMCU ESP8266   │
│                     │
│  ┌──────────────┐   │
│  │   USB Port   │   │  ← USB Cable (Power + Programming)
│  └──────────────┘   │
│                     │
│   WiFi Module       │  ← Connects to WiFi Network
│   (Built-in)        │
│                     │
└─────────────────────┘
         │
         ├─→ Internet
         │
         └─→ Firebase RTDB
```

## 🖥️ Software Setup

### 1. Arduino IDE Configuration

**Install Required Libraries:**
```
- ESP8266WiFi (Built-in with ESP8266 Board Package)
- WiFiClientSecure (Built-in)
- NTPClient by Fabrice Weinberg
- WiFiUdp (Built-in)
```

**Board Settings:**
- Board: "NodeMCU 1.0 (ESP-12E Module)"
- Upload Speed: 115200
- CPU Frequency: 80 MHz
- Flash Size: 4MB (FS:2MB OTA:~1019KB)

### 2. Firebase Configuration

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Navigate to Realtime Database
3. Get your database URL (format: `your-project.firebaseio.com`)
4. Set database rules for testing:
```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

### 3. Code Configuration

Update the following in `RTDB.ino`:

```cpp
// WiFi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Firebase Configuration
const char* FIREBASE_HOST = "your-project-id.firebaseio.com";
const char* FIREBASE_AUTH = ""; // Optional: Add database secret
```

## 📝 Data Structure

### Timestamp Format
```
2025-12-04T01-15-30+06-00
YYYY-MM-DDTHH-MM-SS+TZ-00
```

### Firebase Database Structure
```json
{
  "readings": {
    "2025-12-04T01-15-30+06-00": {
      "data": "your_sensor_data_here"
    }
  }
}
```

## 🚀 Usage

1. **Upload Code:**
   - Connect NodeMCU via USB
   - Select correct COM port in Arduino IDE
   - Upload the sketch

2. **Monitor Serial Output:**
   - Open Serial Monitor (115200 baud)
   - Verify WiFi connection
   - Check Firebase upload status

3. **Verify Data:**
   - Open Firebase Console
   - Navigate to Realtime Database
   - View real-time data updates

## 🔍 Serial Monitor Output

```
WiFi Connecting...
WiFi Connected!
IP: 192.168.1.100
NTP Time Sync: Success
Timestamp: 2025-12-04T01-15-30+06-00
Firebase Upload: Success
```

## 📸 Project Screenshot

![NodeMCU Connected](screenshot.png)
*NodeMCU ESP8266 with USB connection ready for Firebase communication*

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| WiFi not connecting | Check SSID/password, verify 2.4GHz network |
| Firebase upload fails | Verify database URL, check internet connectivity |
| Time sync error | Check NTP server accessibility |
| Compilation error | Install all required libraries |

## 💡 Expansion Ideas

- Add sensor data collection (temperature, humidity, etc.)
- Implement bidirectional control (read commands from Firebase)
- Add OTA (Over-The-Air) updates
- Create web dashboard for visualization
- Implement data analytics and alerts

## 📄 License

This project is open-source and available for educational and commercial use.

## 👨‍💻 Author

IoT Projects Collection
Date: December 2025

---

**Note:** This is a template project. Extend it with your specific sensor implementations and data handling logic.
