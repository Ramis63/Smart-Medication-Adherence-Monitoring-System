# Smart Medication Adherence and Health Monitoring System

A comprehensive health monitoring and medication adherence system available in two modes:
- **Raspberry Pi Mode**: Local Python application with sensors and GPIO
- **Web Platform Mode**: Docker-based web application with Rust backend, React frontend, and SQLite

## Project Overview

This system helps users maintain regular medication intake while monitoring vital signs. The repository contains both a Raspberry Pi implementation (local hardware-based) and a modern web platform (accessible via browser or GitHub Codespaces).

### Two Operating Modes

#### 1. Raspberry Pi Mode (Python + Hardware Sensors)
- Local Python application running on Raspberry Pi 3
- Direct hardware control via GPIO (temperature sensor, heart rate sensor, LED, buzzer, button)
- SQLite database for local data storage
- Standalone operation (no internet required)

#### 2. Web Platform Mode (Rust Backend + React Frontend + Docker)
- Scalable web application accessible from any device with a browser
- Rust backend API with proper error handling and security
- React frontend with responsive UI
- Docker containerization for easy deployment
- GitHub Codespaces support for instant cloud development
- SQLite database (persistent volume in Docker)
- REST API for integration with other systems
- WebSocket support for real-time updates

## Repository Structure

```
smart-medication-system/
├── backend/                      # Rust backend API service
│   ├── src/
│   │   ├── main.rs              # Server entry point
│   │   ├── handlers/            # API route handlers
│   │   ├── models/              # Data models
│   │   ├── middleware/          # Auth & request middleware
│   │   ├── database/            # Database functions
│   │   └── websocket/           # WebSocket handlers
│   ├── Cargo.toml               # Rust dependencies
│   └── Dockerfile               # Backend container image
├── frontend/                     # React frontend application
│   ├── index.html               # Main HTML file
│   ├── css/style.css            # Styling
│   ├── js/
│   │   ├── app.js               # Main application logic
│   │   ├── charts.js            # Data visualization
│   │   ├── websocket.js         # WebSocket client
│   │   └── sanitize.js          # Security utilities
│   └── assets/                  # Static resources
├── docker-compose.yml           # Container orchestration (database, backend, frontend)
├── .devcontainer/
│   └── devcontainer.json        # GitHub Codespaces configuration
├── .github/workflows/
│   └── ci.yml                   # GitHub Actions CI/CD pipeline
├── scripts/
│   └── init-db.sh               # Database initialization script
├── medhealth_system.py          # Raspberry Pi main application
├── add_sample_data.py           # Raspberry Pi data utility
├── requirements.txt             # Python dependencies (for Raspberry Pi)
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
├── QUICK_START.md               # Getting started guide
├── CODESPACES_SETUP.md          # Codespaces instructions
└── REQUIREMENTS_VERIFICATION.md # Compliance documentation
```

## Features

- 💊 **Medication Management**: Add, view, and delete medications with scheduled times
- 🔔 **Smart Alarms**: Visual and audio reminders for medication times
- 📊 **Vital Signs Monitoring**: Monitor body temperature and heart rate
- ⚠️ **Health Alerts**: Automatic alerts when vital signs are abnormal
- 📈 **Data Logging**: Complete history of medication intake and vital signs
- 🎯 **User-Friendly Interface**: Clean menu system (Raspberry Pi) or web UI (Web platform)
- 🔐 **API Key Security**: Environment-based authentication (Web platform)
- 🚀 **Cloud-Ready**: Docker + Codespaces support for instant deployment

---

## Run (Web Mode)

### Quick Start (Local Docker)

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Start all services
docker-compose up -d --build

# 3. Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8080/api/health
```

### Quick Start (GitHub Codespaces)

```bash
# 1. Create a new Codespace from this repository
# 2. Wait for auto-build and auto-start (~1-2 minutes)
# 3. Ports will auto-forward (8080 backend, 3000 frontend)
# 4. Click on port 3000 link to access frontend
```

See [QUICK_START.md](QUICK_START.md) and [CODESPACES_SETUP.md](CODESPACES_SETUP.md) for detailed instructions.

---

## Run (Raspberry Pi Mode)

### System Components

#### Hardware
- **Raspberry Pi 3**
- **DS18B20 Temperature Sensor** (1-wire interface)
- **MAX30102 Heart Rate Sensor** (I2C interface)
- **Active Buzzer** (1x for all alerts)
- **LEDs** (3x - Red for temp, Green for heart rate, Yellow/Blue for button)
- **Push Button** (for medication confirmation)
- **Resistors** (220Ω for LEDs, 4.7kΩ for DS18B20 pull-up, 10kΩ for button)

#### Software
- Python 3.x
- SQLite database
- GPIO libraries for Raspberry Pi
- Sensor libraries (Adafruit CircuitPython)

### Installation

#### 1. Enable Required Interfaces

```bash
sudo raspi-config
```

Enable:
- **I2C** (for MAX30102 heart rate sensor)
- **1-Wire** (for DS18B20 temperature sensor)

#### 2. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev
pip3 install -r requirements.txt
```

#### 3. Wire Components

Connect hardware according to Pin Connections Summary below.

#### 4. Run the System

```bash
sudo python3 medhealth_system.py
```

**Note:** `sudo` is required for GPIO access.

### System Workflow (Raspberry Pi)

#### Main Menu Options

1. **➕ Add Medication**: Schedule a new medication with time
2. **📋 View Medications**: Display all active medications
3. **🗑️ Delete Medication**: Remove a medication from schedule
4. **📊 Measure Vitals (Manual)**: Check temperature and heart rate without logging
5. **📈 View Medication History**: View last 20 medication logs with vital signs
6. **🧪 Test Menu**: 
   - Test Alarm (LEDs + Buzzer)
   - Test Button (Real-time press/release testing)
7. **🚀 Start Monitoring**: Begin health monitoring (vitals only)
   - **Note:** Medication alarms work automatically and independently
8. **🚪 Exit**: Safely shutdown system

#### Independent Medication Alarm System

**Alarms work automatically** - No need to start monitoring!
- Runs in background thread when system starts
- Checks every 5 seconds for accurate timing
- 30-second time window (catches alarms even if check happens slightly before/after)
- Uses PWM buzzer for clear, audible tones (2000 Hz)

#### Medication Alarm Flow (Automatic)

1. **Automatic Detection:**
   - System checks every 5 seconds (high accuracy)
   - Triggers if within 30 seconds of scheduled time (before or after)
   - Works automatically when system starts

2. When scheduled time arrives:
   - Blue LED near button blinks
   - Buzzer sounds with clear PWM tone
   - System waits up to 60 seconds for button press
   - Console displays medication reminder banner

3. When button is pressed:
   - Alarm stops immediately
   - Blue LED turns ON + continuous beep for 2 seconds (confirmation)
   - System asks: "Measure vitals now?"

4. If button pressed within 5 seconds (for vitals):
   - Measures temperature and heart rate
   - Saves medication log with vital signs

5. If no button press (5 seconds - skip vitals):
   - Saves medication log without vital signs
   - Status: "taken"
   - Alarm monitoring continues automatically

6. If no button press (60 seconds - missed):
   - Medication marked as "missed"
   - Logged without vital signs
   - Alarm monitoring continues automatically

#### Health Monitoring (Option 7 - Optional)

**Note:** This is separate from medication alarms. Alarms work independently.

When monitoring is active (Option 7):
- **Health monitoring**: Every 10 seconds (temperature & heart rate)
- **Dashboard updates**: Every 30 seconds
- **Shows**: Active medications and countdown

**Abnormal Conditions:**
- **Temperature** < 18°C or > 30°C:
  - Red LED (near temp sensor) blinks
  - Buzzer sounds
  - Console alert displayed

- **Heart Rate** < 60 bpm or > 120 bpm:
  - Green LED (near heart sensor) blinks
  - Buzzer sounds
  - Console alert displayed

### Pin Connections Summary

| Component | Physical Pin | GPIO Pin |
|-----------|--------------|----------|
| DS18B20 DATA | 7 | GPIO 4 |
| MAX30102 SDA | 3 | GPIO 2 |
| MAX30102 SCL | 5 | GPIO 3 |
| Buzzer | 11 | GPIO 17 |
| Button | 13 | GPIO 27 |
| LED Heart | 15 | GPIO 22 |
| LED Temp | 16 | GPIO 23 |
| LED Button | 18 | GPIO 24 |

---

## Data & Storage

### Database

Both modes use SQLite with the same schema:

1. **medications**: Stores medication schedules
   - id, name, schedule_time, active, created_at

2. **medication_logs**: Records medication intake with timestamps and vital signs
   - id, medication_id, medication_name, scheduled_time, actual_time, status, temperature, heart_rate, created_at

3. **vitals_logs**: Stores standalone vital sign measurements
   - id, temperature, heart_rate, status, created_at

### API Data Format (Web Platform)

- **Request/Response Format**: JSON
- **Authentication**: Bearer token via `Authorization` header
- **Sample Endpoints**:
  - GET `/api/medications` - Retrieve all medications
  - POST `/api/medications` - Create new medication
  - POST `/api/vitals` - Log vital signs
  - GET `/api/health` - Health check

### Local Storage (Raspberry Pi)

- SQLite database file: `medhealth.db`
- JSON export via `add_sample_data.py` script for backups

---

## Security & Medical Disclaimer

⚠️ **IMPORTANT**: This system is designed for **educational and personal health awareness purposes only**. It does NOT provide medical diagnosis or treatment. Always consult healthcare professionals for medical advice.

### Security Notes (Web Platform)

- Database URL configured via environment variables (not hardcoded)
- API key authentication required for all endpoints
- `.env` file is gitignored and not committed to repository
- Use `.env.example` as template for your configuration

---

## Troubleshooting (Raspberry Pi)

### Sensors Not Detected
- Verify I2C and 1-Wire are enabled: `sudo raspi-config`
- Check connections with: `i2cdetect -y 1` and `ls /sys/bus/w1/devices/`

### LEDs/Buzzer Not Working
- Verify GPIO pin connections
- Check resistor values (220Ω for LEDs)
- Ensure proper power supply

### Button Not Responding
- Verify pull-up configuration
- Check button connections (GPIO to GND when pressed)

---

## Team Members

- **Muhammad Ramis Chaudhary** (Project Owner) — 22401363
- **Zainab Malik** — 22402832
- **Batool Saad Jalal Qaba** — 22412036

---

## License

This project is for educational purposes as part of a Health Informatics course at TH Deggendorf.

## Additional Resources

- [Quick Start Guide](QUICK_START.md) - Getting started with Docker/Codespaces
- [Codespaces Setup](CODESPACES_SETUP.md) - Cloud development environment
- [Requirements Verification](REQUIREMENTS_VERIFICATION.md) - Professor requirements compliance


