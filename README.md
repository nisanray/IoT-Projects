# IoT Projects Collection

![IoT](https://img.shields.io/badge/Category-Internet%20of%20Things-blue)
![Platform](https://img.shields.io/badge/Platform-ESP8266%20%7C%20Arduino-green)
![Database](https://img.shields.io/badge/Database-Firebase%20RTDB-orange)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Overview

A comprehensive collection of Internet of Things (IoT) projects demonstrating real-world applications of microcontroller programming, sensor integration, cloud connectivity, and web-based monitoring systems. Each project showcases professional development practices with complete documentation, circuit diagrams, and production-ready code.

## 🗂️ Projects

### 1. 🌐 NodeMCU Firebase RTDB Template
**Path:** `NodeMCU_RTDB_/`

A foundational template demonstrating ESP8266 WiFi connectivity and Firebase Realtime Database integration.

**Key Features:**
- WiFi connectivity with auto-reconnection
- Firebase RTDB real-time synchronization
- NTP time synchronization (GMT+6)
- Custom timestamp formatting
- Secure HTTPS communication

**Hardware:**
- NodeMCU ESP8266

**Use Case:** Starting point for any IoT project requiring cloud connectivity

[📖 Full Documentation](NodeMCU_RTDB_/README.md)

---

### 2. 🏠 Smart Hall IoT Automation System
**Path:** `Smart Hall/`

An intelligent building automation system with occupancy detection, environmental monitoring, and automatic lighting/HVAC control.

**Key Features:**
- Bidirectional IR people counting
- DHT11 temperature & humidity monitoring
- Automatic LED control based on light and occupancy
- Temperature-based HVAC/motor speed control
- Web dashboard with manual override
- Emergency stop functionality

**Hardware:**
- NodeMCU ESP8266
- DHT11 Sensor
- 2× IR Obstacle Sensors
- LDR (Light Sensor)
- LED with PWM control
- DC Motor/Fan

**Use Case:** Smart building automation, energy management, occupancy monitoring

[📖 Full Documentation](Smart%20Hall/README.md)

---

### 3. 🌦️ Weather Monitoring Station
**Path:** `Weather Monitoring/`

A multi-sensor environmental monitoring system with dual microcontrollers for comprehensive data logging and cloud storage.

**Key Features:**
- Dual temperature sensors (DHT11 + BMP280)
- Humidity, pressure, and altitude measurement
- Rain detection (digital + analog)
- Light intensity measurement (LDR)
- Real-time and historical data dashboards
- CSV export functionality
- 30-second automatic data logging

**Hardware:**
- Arduino Uno (Sensor Hub)
- NodeMCU ESP8266 (WiFi Gateway)
- DHT11 Sensor
- BMP280 Sensor (I2C)
- Rain Sensor Module
- LDR Module

**Use Case:** Weather station, environmental monitoring, climate data collection

[📖 Full Documentation](Weather%20Monitoring/README.md)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      IoT PROJECTS ECOSYSTEM                     │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐        ┌──────────────────────┐
│  Microcontrollers    │        │   Sensors & I/O      │
│  ─────────────────   │        │   ───────────────    │
│  • NodeMCU ESP8266   │◄──────►│  • DHT11 (Temp/Hum)  │
│  • Arduino Uno       │        │  • BMP280 (Pressure) │
│  • WiFi Built-in     │        │  • IR Sensors        │
│  • Serial Comm       │        │  • LDR (Light)       │
└──────────┬───────────┘        │  • Rain Sensor       │
           │                    │  • LED/Motor (PWM)   │
           │                    └──────────────────────┘
           ▼
┌──────────────────────┐
│   Cloud Services     │
│   ──────────────     │
│  • Firebase RTDB     │
│  • NTP Time Sync     │
│  • HTTPS/TLS         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Web Dashboards     │
│   ──────────────     │
│  • Real-time Monitor │
│  • Historical Data   │
│  • Manual Controls   │
│  • Data Export       │
└──────────────────────┘
```

## 🔧 Common Technologies

### Hardware Platforms
- **NodeMCU ESP8266** - WiFi-enabled microcontroller (ESP-12E module)
- **Arduino Uno** - ATmega328P for multi-sensor applications

### Communication Protocols
- **WiFi** - 2.4GHz 802.11 b/g/n
- **UART Serial** - Inter-MCU communication (9600 baud)
- **I2C** - Sensor bus (BMP280)
- **HTTPS/TLS** - Secure cloud communication

### Cloud Platform
- **Firebase Realtime Database** - NoSQL cloud database
- **NTP** - Network Time Protocol for synchronization

### Programming
- **Arduino C/C++** - Firmware development
- **HTML/CSS/JavaScript** - Web dashboards
- **Firebase SDK** - Cloud integration

## 📚 Documentation

Each project folder contains:
- ✅ **README.md** - Complete project documentation
- ✅ **Circuit diagrams** - ASCII and visual schematics
- ✅ **Pin configuration** - Detailed wiring tables
- ✅ **Source code** - Fully commented Arduino sketches
- ✅ **Web interfaces** - HTML dashboards
- ✅ **Screenshot guides** - Photography instructions

## 🚀 Getting Started

### Prerequisites

**Software:**
1. [Arduino IDE](https://www.arduino.cc/en/software) 2.0 or higher
2. ESP8266 Board Package
3. Required libraries (listed in each project)

**Hardware:**
- ESP8266 NodeMCU development board(s)
- Arduino Uno (for Weather Station)
- Sensors (project-specific)
- USB cables (Micro USB, Type-A to Type-B)
- Breadboards and jumper wires
- 5V power supply (2A recommended)

**Cloud Services:**
- [Firebase](https://firebase.google.com/) account (free tier sufficient)

### Quick Start

1. **Choose a project** from the list above
2. **Read the project README** for specific requirements
3. **Set up Firebase:**
   - Create project at Firebase Console
   - Enable Realtime Database
   - Get configuration credentials
4. **Assemble hardware** following circuit diagrams
5. **Install required libraries** via Arduino IDE
6. **Update configuration:**
   - WiFi credentials
   - Firebase settings
7. **Upload code** to microcontroller(s)
8. **Open web dashboard** to monitor

## 📊 Project Comparison

| Feature | NodeMCU Template | Smart Hall | Weather Station |
|---------|------------------|------------|-----------------|
| **Complexity** | Beginner | Intermediate | Advanced |
| **Microcontrollers** | 1 (ESP8266) | 1 (ESP8266) | 2 (Uno + ESP8266) |
| **Sensors** | None (template) | 4 (DHT, IR×2, LDR) | 4 (DHT, BMP, Rain, LDR) |
| **Outputs** | None | 2 (LED, Motor) | None |
| **Web Interface** | No | Yes (Control) | Yes (Monitor) |
| **Data Logging** | Yes | Status only | Yes (Historical) |
| **Real-time Control** | No | Yes | No |
| **Setup Time** | 30 min | 2-3 hours | 3-4 hours |

## 🛠️ Common Components

### Essential Items for All Projects
- NodeMCU ESP8266 (CP2102 or CH340 driver)
- Micro USB cables
- Breadboards (830 points recommended)
- Jumper wires (M-M, M-F)
- 10kΩ resistors (pull-ups)
- 220Ω resistors (LED current limiting)

### Optional but Recommended
- Multimeter (for debugging)
- Logic analyzer (for serial/I2C debugging)
- Soldering iron (for permanent installations)
- Heat shrink tubing
- Project enclosures
- Power supply module (MB102 breadboard power)

## 📈 Learning Path

### Beginner → Advanced

1. **Start with:** NodeMCU Firebase RTDB Template
   - Learn WiFi connectivity
   - Understand Firebase basics
   - Practice serial debugging

2. **Progress to:** Smart Hall Automation
   - Sensor integration (DHT11, IR, LDR)
   - PWM output control
   - Web-based monitoring and control
   - State management

3. **Master with:** Weather Monitoring Station
   - Multi-microcontroller systems
   - I2C communication
   - Serial inter-MCU communication
   - Complex data structures
   - Historical data management

## 🔐 Security Considerations

### Development Phase
- Public Firebase rules for testing
- WiFi credentials in code (not for production)

### Production Deployment
- ✅ Enable Firebase Authentication
- ✅ Implement secure database rules
- ✅ Use environment variables for secrets
- ✅ Enable HTTPS for web hosting
- ✅ Add API key restrictions
- ✅ Implement user authentication

**Example Production Rules:**
```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null && auth.uid === 'authorized_user_id'"
  }
}
```

## 🐛 Troubleshooting

### Common Issues Across Projects

**WiFi Connection Failures:**
- Verify 2.4GHz network (ESP8266 doesn't support 5GHz)
- Check SSID/password accuracy
- Ensure strong signal strength
- Try static IP if DHCP fails

**Firebase Upload Errors:**
- Verify database URL format
- Check internet connectivity
- Confirm Firebase rules allow writes
- Monitor serial output for errors

**Sensor Reading Issues:**
- Verify correct pin connections
- Check power supply voltage (3.3V vs 5V)
- Add pull-up resistors where needed
- Test sensors individually

**Upload/Compilation Errors:**
- Install correct board package
- Select proper board and port
- Update all libraries to latest versions
- Check for conflicting libraries

## 💡 Enhancement Ideas

### Cross-Project Features
- [ ] **Mobile Apps** - Native Android/iOS applications
- [ ] **Voice Control** - Alexa/Google Home integration
- [ ] **MQTT Protocol** - Alternative to Firebase for local control
- [ ] **OTA Updates** - Over-the-air firmware updates
- [ ] **Power Monitoring** - Battery status and solar charging
- [ ] **Multi-location** - Deploy multiple stations
- [ ] **Data Analytics** - Machine learning predictions
- [ ] **Alerts** - Email/SMS notifications
- [ ] **LoRa Communication** - Long-range wireless
- [ ] **Local Storage** - SD card backup

## 📖 Additional Resources

### Documentation
- [ESP8266 Arduino Core Documentation](https://arduino-esp8266.readthedocs.io/)
- [Firebase Realtime Database Guide](https://firebase.google.com/docs/database)
- [Arduino Reference](https://www.arduino.cc/reference/en/)

### Community
- [ESP8266 Community Forum](https://www.esp8266.com/)
- [Arduino Forum](https://forum.arduino.cc/)
- [Firebase Community](https://firebase.google.com/community)

### Learning
- [ESP8266 Tutorials](https://randomnerdtutorials.com/projects-esp8266/)
- [Arduino Project Hub](https://create.arduino.cc/projecthub)
- [Firebase Web Codelab](https://firebase.google.com/codelabs)

## 📄 License

All projects in this collection are open-source and available for educational and commercial use. Feel free to modify, extend, and distribute.

## 👨‍💻 Author

**IoT Projects Collection**
- Platform: ESP8266 & Arduino
- Database: Firebase Realtime Database
- Version: 1.0
- Last Updated: December 2025

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to:
- Report bugs
- Suggest enhancements
- Submit pull requests
- Share your modifications

## 📞 Support

For project-specific help, refer to individual project README files. Each contains detailed troubleshooting sections and configuration guides.

---

**⚡ Quick Links:**
- [NodeMCU Template](NodeMCU_RTDB_/) | [Smart Hall](Smart%20Hall/) | [Weather Station](Weather%20Monitoring/)

**🎯 Remember:** Start simple, test thoroughly, and build incrementally. Each project builds on the previous one's concepts!
