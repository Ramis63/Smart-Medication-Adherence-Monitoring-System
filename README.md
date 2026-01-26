# Smart Medication Adherence and Health Monitoring System

A Raspberry Pi 3-based system designed to help users maintain regular medication intake while monitoring basic vital signs (body temperature and heart rate).

## Features

- 💊 **Medication Management**: Add, view, and delete medications with scheduled times
- 🔔 **Smart Alarms**: Visual (LED) and audio (buzzer) reminders for medication times
- 📊 **Vital Signs Monitoring**: Continuous monitoring of body temperature and heart rate
- ⚠️ **Health Alerts**: Automatic alerts when vital signs are abnormal
- 📈 **Data Logging**: Complete history of medication intake and vital signs
- 🎯 **User-Friendly Interface**: Clean menu system with emoji indicators

## System Components

### Hardware
- **Raspberry Pi 3**
- **DS18B20 Temperature Sensor** (1-wire interface)
- **MAX30102 Heart Rate Sensor** (I2C interface)
- **Active Buzzer** (1x for all alerts)
- **LEDs** (3x - Red for temp, Green for heart rate, Yellow/Blue for button)
- **Push Button** (for medication confirmation)
- **Resistors** (220Ω for LEDs, 4.7kΩ for DS18B20 pull-up, 10kΩ for button)

### Software
- Python 3.x
- SQLite database
- GPIO libraries for Raspberry Pi
- Sensor libraries (Adafruit CircuitPython)

## Installation

### 1. Enable Required Interfaces

```bash
sudo raspi-config
```

Enable:
- **I2C** (for MAX30102 heart rate sensor)
- **1-Wire** (for DS18B20 temperature sensor)

### 2. Install Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev
pip3 install -r requirements.txt
```

### 3. Wire Components

Follow the detailed wiring guide in `WIRING_GUIDE.md` or the PDF documentation.

### 4. Run the System

```bash
sudo python3 medhealth_system.py
```

**Note:** `sudo` is required for GPIO access.

## System Workflow

### Main Menu Options

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

### Independent Medication Alarm System ⭐ NEW

**Alarms work automatically** - No need to start monitoring!
- Runs in background thread when system starts
- Checks every 5 seconds for accurate timing
- 30-second time window (catches alarms even if check happens slightly before/after)
- Uses PWM buzzer for clear, audible tones (2000 Hz)

### Medication Alarm Flow (Automatic)

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

### Health Monitoring (Option 7 - Optional)

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

## Pin Connections Summary

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

## Database Schema

The system uses SQLite with three tables:

1. **medications**: Stores medication schedules
2. **medication_logs**: Records medication intake with timestamps and vital signs
3. **vitals_logs**: Stores standalone vital sign measurements

## Safety & Medical Disclaimer

⚠️ **IMPORTANT**: This system is designed for **educational and personal health awareness purposes only**. It does NOT provide medical diagnosis or treatment. Always consult healthcare professionals for medical advice.

## Troubleshooting

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

## License

This project is for educational purposes as part of a Health Informatics course.

## Author

Developed for Media Management project at TH Deggendorf.

