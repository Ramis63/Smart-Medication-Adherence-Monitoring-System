# Smart Medication Adherence and Health Monitoring System
## Complete Documentation & Setup Guide

---

**Project:** Smart Medication Adherence and Health Monitoring System  
**Platform:** Raspberry Pi 3  
**Purpose:** Educational Health Informatics Tool  
**Version:** 3.0 (Independent Alarm System & Enhanced Features)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [System Features](#system-features)
3. [Hardware Components](#hardware-components)
4. [Wiring Instructions](#wiring-instructions)
5. [Software Installation](#software-installation)
6. [System Workflow](#system-workflow)
7. [Technical Specifications](#technical-specifications)
8. [Safety & Medical Disclaimer](#safety--medical-disclaimer)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

The Smart Medication Adherence and Health Monitoring System is a Raspberry Pi 3-based solution designed to help users maintain regular medication intake while observing basic personal health parameters. The system provides:

- **Timed medication reminders** using visual (LED) and audio (buzzer) alerts
- **Medication intake confirmation** via button press with automatic logging
- **Continuous vital signs monitoring** (body temperature and heart rate)
- **Automatic health alerts** when vital signs are abnormal
- **Data visualization** through stored logs and history

**Important:** This system focuses solely on observation and monitoring for personal health awareness. It does NOT provide medical diagnosis or treatment, making it a low-cost, practical, and educational Health Informatics tool.

---

## System Features

### Core Functionality

1. **Medication Management**
   - Add medications with scheduled times (HH:MM format)
   - View all active medications
   - Delete medications from schedule
   - Automatic duplicate prevention (one alarm per day per medication)

2. **Independent Smart Alarm System** ⭐ NEW
   - **Runs automatically** - No need to start monitoring for alarms
   - Visual alerts: Blue LED blinking near button
   - Audio alerts: Buzzer sounds with PWM for clear tone
   - Checks every 5 seconds for accurate timing
   - 30-second time window (catches alarms even if check happens slightly before/after)
   - 60-second alarm duration
   - Button press to confirm intake
   - 2-second continuous beep + Blue LED ON when medication taken (confirmation)
   - Works independently of "Start Monitoring" option

3. **Vital Signs Monitoring**
   - **Body Temperature**: Measured using DS18B20 sensor (°C)
   - **Heart Rate**: Measured using MAX30102 sensor (BPM)
   - Continuous monitoring every 10 seconds
   - Manual measurement option available

4. **Health Alerts**
   - **Temperature Abnormal**: < 18°C or > 30°C
     - Red LED (near temp sensor) blinks
     - Buzzer sounds
   - **Heart Rate Abnormal**: < 60 bpm or > 120 bpm
     - Green LED (near heart sensor) blinks
     - Buzzer sounds

5. **Data Logging**
   - Medication intake logs with timestamps
   - Optional vital signs recorded with medication intake
   - View last 20 medication entries
   - Complete history with scheduled vs actual times

6. **User Interface**
   - Clean menu system with 8 options
   - Emoji indicators for better UX
   - Real-time status updates
   - Graceful error handling

---

## Hardware Components

### Required Components

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Raspberry Pi 3 | 1 | Main controller |
| DS18B20 Temperature Sensor | 1 | Body temperature measurement |
| MAX30102 Heart Rate Sensor | 1 | Heart rate measurement (BPM) |
| Active Buzzer | 1 | Audio alerts (all functions) |
| LED (Red) | 1 | Temperature sensor indicator |
| LED (Green) | 1 | Heart rate sensor indicator |
| LED (Blue) | 1 | Button/medication indicator (near button) |
| Push Button | 1 | Medication confirmation |
| Resistor 220Ω | 3 | LED current limiting |
| Resistor 4.7kΩ | 1 | DS18B20 pull-up |
| Breadboard | 1 | Component mounting |
| Jumper Wires | ~20 | Connections |

### Component Specifications

**DS18B20 Temperature Sensor**
- Interface: 1-Wire
- Range: -55°C to +125°C
- Accuracy: ±0.5°C
- Power: 3.0V to 5.5V

**MAX30102 Heart Rate Sensor**
- Interface: I2C
- Measures: Heart rate (BPM), SpO2
- Power: 3.3V or 5V (check module specs)
- Sampling rate: Programmable

**Buzzer**
- Type: Active buzzer (5V)
- Sound: ~2.5kHz tone
- Current: ~30mA

**LEDs**
- Type: Standard 5mm LEDs
- Current: ~20mA (with 220Ω resistor)
- Colors: Red (near temperature sensor), Green (near heart sensor), Blue (near button)

---

## Wiring Instructions

### Physical Pin Numbering

**IMPORTANT:** This guide uses **Physical Pin Numbers** (not GPIO numbers) as requested.

### Pin Connection Table

| Component | Physical Pin | GPIO Pin | Notes |
|-----------|--------------|----------|-------|
| DS18B20 DATA | **7** | GPIO 4 | 1-Wire Data |
| MAX30102 SDA | **3** | GPIO 2 | I2C Data |
| MAX30102 SCL | **5** | GPIO 3 | I2C Clock |
| Buzzer (+) | **11** | GPIO 17 | Output |
| Button | **13** | GPIO 27 | Input (Pull-up) |
| LED Heart (Green) | **15** | GPIO 22 | Output |
| LED Temp (Red) | **16** | GPIO 23 | Output |
| LED Button (Blue) | **18** | GPIO 24 | Output |
| 5V Power | **2** | - | Power supply |
| 3.3V Power | **1** | - | MAX30102 power |
| GND | **6** | - | Common ground |

### Detailed Wiring Steps (64-Row Breadboard)

#### Step 1: Power Connections
1. Connect **Physical Pin 2 (5V)** to **LEFT power rail (+)**
2. Connect **Physical Pin 6 (GND)** to **LEFT power rail (-)**
3. **Optional**: Connect left and right power rails together for easier wiring

#### Step 2: DS18B20 Temperature Sensor (Rows 1-4)
**IMPORTANT:** Each pin must be in a **separate row** because rows connect all columns together.
**NOTE:** Wire order (soldered): Red (VDD), Black (GND) in middle, Yellow (DATA)

1. **Row 1, Column A**: VDD (Red wire) → Connect to power rail (+)
2. **Row 2, Column A**: GND (Black wire) → Connect to power rail (-)
3. **Row 3, Column A**: DATA (Yellow wire) → Connect to **Physical Pin 7 (GPIO 4)**
4. **Row 4**: Place 4.7kΩ pull-up resistor:
   - **Column A**: One end of resistor
   - **Column B**: Other end of resistor → Connect to power rail (+)
   - **Column C**: Jumper wire to Row 3-A (DATA line)

#### Step 3: MAX30102 Heart Rate Sensor (Rows 6-9)
**IMPORTANT:** Each pin must be in a **separate row** to avoid short circuits.

1. **Row 6, Column A**: VIN → Connect to **Physical Pin 1 (3.3V)** or **Pin 2 (5V)**
2. **Row 7, Column A**: GND → Connect to power rail (-)
3. **Row 8, Column A**: SDA → Connect to **Physical Pin 3 (GPIO 2 / SDA)**
4. **Row 9, Column A**: SCL → Connect to **Physical Pin 5 (GPIO 3 / SCL)**

#### Step 4: Green LED - Heart Sensor (Rows 11-13)
**IMPORTANT:** LED anode and cathode must be in **separate rows** to avoid short circuit.

1. **Row 11**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 15 (GPIO 22)**
   - **Column B**: Other end (resistor output)

2. **Row 12, Column A**: Green LED Anode (+) (near MAX30102 heart sensor) → Jumper wire to Row 11-B
3. **Row 13, Column A**: Green LED Cathode (-) → Connect to power rail (-)

#### Step 5: Red LED - Temperature Sensor (Rows 16-18)
**IMPORTANT:** LED anode and cathode must be in **separate rows** to avoid short circuit.

1. **Row 16**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 16 (GPIO 23)**
   - **Column B**: Other end (resistor output)

2. **Row 17, Column A**: Red LED Anode (+) (near DS18B20 temperature sensor) → Jumper wire to Row 16-B
3. **Row 18, Column A**: Red LED Cathode (-) → Connect to power rail (-)

#### Step 6: Blue LED - Button (Rows 21-23)
**IMPORTANT:** LED anode and cathode must be in **separate rows** to avoid short circuit.

1. **Row 21**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 18 (GPIO 24)**
   - **Column B**: Other end (resistor output)

2. **Row 22, Column A**: Blue LED Anode (+) (near button) → Jumper wire to Row 21-B
3. **Row 23, Column A**: Blue LED Cathode (-) → Connect to power rail (-)

#### Step 7: Push Button (Row 26)
1. **Row 26**: Place push button:
   - **Column A-B**: Button Terminal 1 (same row, connected internally)
   - **Column D-E**: Button Terminal 2 (same row, connected internally)
   - Connect **Column A** to **Physical Pin 13 (GPIO 27)**
   - Connect **Column E** to power rail (-)
   - **Note:** Internal pull-up is enabled in code, so button pulls GPIO LOW when pressed

#### Step 8: Buzzer (Rows 31-32)
**IMPORTANT:** Buzzer positive and negative must be in **separate rows** to avoid short circuit.

1. **Row 31, Column A**: Buzzer Positive (+) terminal → Connect to **Physical Pin 11 (GPIO 17)**
   - **Optional**: Add 220Ω resistor in series if needed
2. **Row 32, Column A**: Buzzer Negative (-) terminal → Connect to power rail (-)

**Wiring Tips:**
- Use jumper wires to connect components on the same row
- All GND connections go to power rail (-)
- Keep components organized by rows for easier troubleshooting
- Leave space between component groups for clarity

### Breadboard Layout Diagram

**Note:** This system is designed for a standard breadboard with **64 rows and 5 columns (A-E)**. The detailed row-by-row placement guide is provided below.

**Standard Breadboard Structure:**
- **Power Rails**: Left and right sides (Red = +, Blue/Black = -)
- **Main Area**: Rows 1-64, Columns A-E (left side) and A-E (right side)
- **Center Gap**: Separates left and right sections (for DIP ICs)

**Recommended Component Placement by Row:**

| Row Range | Component | Details |
|-----------|-----------|---------|
| **Power Rails** | Left/Right sides | Red (+) and Black (-) rails |
| **Row 1** | DS18B20 VDD | A: VDD (Red) to Power Rail + |
| **Row 2** | DS18B20 GND | A: GND (Black) to Power Rail - |
| **Row 3** | DS18B20 DATA | A: DATA (Yellow) to Pin 7 |
| **Row 4** | 4.7kΩ Resistor | Pull-up for DS18B20 DATA |
| **Row 6** | MAX30102 VIN | A: VIN to Pin 1/2 |
| **Row 7** | MAX30102 GND | A: GND to Power Rail - |
| **Row 8** | MAX30102 SDA | A: SDA to Pin 3 |
| **Row 9** | MAX30102 SCL | A: SCL to Pin 5 |
| **Row 11** | 220Ω Resistor | For Green LED |
| **Row 12** | Green LED Anode | Heart sensor (near MAX30102) |
| **Row 13** | Green LED Cathode | To Power Rail - |
| **Row 16** | 220Ω Resistor | For Red LED |
| **Row 17** | Red LED Anode | Temperature sensor (near DS18B20) |
| **Row 18** | Red LED Cathode | To Power Rail - |
| **Row 21** | 220Ω Resistor | For Blue LED |
| **Row 22** | Blue LED Anode | Button indicator (near button) |
| **Row 23** | Blue LED Cathode | To Power Rail - |
| **Row 26** | Push Button | Medication confirmation |
| **Row 31** | Buzzer Positive | To Pin 11 |
| **Row 32** | Buzzer Negative | To Power Rail - |
| **Row 36-64** | Available | For future expansion |

**For complete detailed wiring instructions with exact row and column positions, see `WIRING_GUIDE.md` or `BREADBOARD_LAYOUT_DETAILED.md`**

```
                    Raspberry Pi 3
    ┌─────────────────────────────────────────┐
    │  [1] 3.3V  [2] 5V   [3] SDA  [4] 5V   │
    │  [5] SCL   [6] GND  [7] GPIO4 [8]     │
    │  [9] GND   [10]     [11] GPIO17 [12]  │
    │  [13] GPIO27 [14] GND [15] GPIO22 [16]│
    │  [17] GPIO23 [18] GPIO24 [19] [20] GND│
    └─────────────────────────────────────────┘
                    │
                    │ Jumper Wires
                    ▼
    ┌─────────────────────────────────────────┐
    │         BREADBOARD (64 Rows, A-E)        │
    │                                         │
    │  Power Rail + ← Pin 2 (5V)             │
    │  Power Rail - ← Pin 6 (GND)            │
    │                                         │
    │  Row 1-2:   DS18B20 + 4.7kΩ            │
    │  Row 6:     MAX30102                    │
    │  Row 11-12: Green LED (Heart - near MAX30102) │
    │  Row 16-17: Red LED (Temp - near DS18B20)     │
    │  Row 21-22: Blue LED (Button - near button)   │
    │  Row 26:    Push Button                 │
    │  Row 31:    Buzzer                      │
    │  Row 36-64: Available                   │
    └─────────────────────────────────────────┘
```

### Safety Checklist

- [ ] Double-check all connections before powering on
- [ ] Verify resistor values (220Ω for LEDs, 4.7kΩ for DS18B20)
- [ ] Ensure all GND connections are connected to common ground
- [ ] Check sensor voltage requirements (3.3V vs 5V)
- [ ] Test each component individually before full system test
- [ ] Verify LED polarity (anode/cathode)
- [ ] Ensure button connects GPIO to GND (not VCC)

---

## Software Installation

### Prerequisites

- Raspberry Pi 3 with Raspberry Pi OS installed
- Internet connection for package installation
- Python 3.x (usually pre-installed)

### Step 1: Enable Required Interfaces

```bash
sudo raspi-config
```

Navigate to:
- **Interface Options** → **I2C** → Enable
- **Interface Options** → **1-Wire** → Enable

Reboot if prompted:
```bash
sudo reboot
```

### Step 2: Verify Interfaces

**Check I2C (for MAX30102):**
```bash
sudo i2cdetect -y 1
```
Should show device addresses (typically 0x57 for MAX30102).

**Check 1-Wire (for DS18B20):**
```bash
ls /sys/bus/w1/devices/
```
Should show device directories (e.g., `28-xxxxx`).

### Step 3: Install Python Dependencies

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev python3-smbus

pip3 install -r requirements.txt
```

### Step 4: Install System Files

Copy `medhealth_system.py` to your Raspberry Pi:
```bash
# On Raspberry Pi
nano medhealth_system.py
# Paste code and save
```

Make executable:
```bash
chmod +x medhealth_system.py
```

### Step 5: Run the System

```bash
sudo python3 medhealth_system.py
```

**Note:** `sudo` is required for GPIO access.

---

## System Workflow

### Main Menu

```
💊 MEDHEALTH SYSTEM
═══════════════════════════════════════════════════════════
1. ➕ Add Medication
2. 📋 View Medications
3. 🗑️ Delete Medication
4. 📊 Measure Vitals (Manual)
5. 📈 View Medication History
6. 🧪 Test Alarm
7. 🚀 Start Monitoring
8. 🚪 Exit
═══════════════════════════════════════════════════════════
```

### Option 1: Add Medication

1. Select option 1
2. Enter medication name (e.g., "Aspirin")
3. Enter schedule time in HH:MM format (e.g., "08:00")
4. Medication added to database

### Option 2: View Medications

Displays all active medications with:
- Medication ID
- Medication name
- Scheduled time
- Current status (✓ Taken / ✗ Missed / ⏰ Pending / ⏳ Upcoming)
- Date and current time header
- Total count of active medications

**Note:** Press Enter to continue after viewing.

### Option 3: Delete Medication

1. View medications first (option 2)
2. Select option 3
3. Enter medication ID to delete
4. Medication marked as inactive

### Option 4: Measure Vitals (Manual)

- Measures temperature instantly
- Measures heart rate (waits up to 10 seconds)
- Displays results on screen
- **Not saved to database** (for checking only)

### Option 5: View Medication History

Shows last 20 medication logs with:
- Medication name and status (✓ TAKEN / ✗ MISSED)
- Scheduled vs actual time
- Temperature and heart rate (if measured)
- Full timestamp (date and time)
- Statistics summary:
  - Total entries
  - Taken vs Missed count
  - Entries with vital signs

**Display Format:**
- Professional table layout
- Clear status indicators
- Formatted date/time display
- Statistics at the bottom

**Note:** Press Enter to continue after viewing.

Example log entry:
```
Aspirin              08:00        08:15:32     ✓ TAKEN    T:36.7°C HR:72bpm   2024-01-15 08:15:32
```

### Option 6: Test Menu

**Submenu Options:**
1. **Test Alarm** - Test all LEDs and buzzer
   - All LEDs blink for 3 seconds
   - Buzzer sounds for 3 seconds
   - Useful for verifying hardware connections

2. **Test Button** - Real-time button testing ⭐ NEW
   - Press button → Blue LED turns ON + Buzzer sounds
   - Release button → Blue LED turns OFF + Buzzer stops
   - Shows press/release counters
   - Tests button connection on startup
   - Press Ctrl+C to exit

3. **Back to Main Menu**

### Option 7: Start Monitoring (Health Monitoring Only)

**IMPORTANT:** Medication alarms work independently and automatically. This option only starts health monitoring.

**Background Processes:**
- **Health monitoring**: Checks temperature and heart rate every 10 seconds
- **Dashboard updates**: Every 30 seconds
- **Medication alarms**: Continue running independently (not affected by this option)

**Note:** Medication alarms run automatically in the background. You don't need to start monitoring for alarms to work.

**Medication Alarm Flow (Automatic):**
1. **Alarm Detection:**
   - System checks every 5 seconds (improved accuracy)
   - Triggers if within 30 seconds of scheduled time (before or after)
   - Works automatically when system starts

2. When scheduled time arrives:
   - Blue LED near button blinks
   - Buzzer sounds with PWM tone (clear, audible beeping pattern)
   - System waits up to 60 seconds
   - Console displays medication reminder banner

3. User presses button to confirm:
   - Alarm stops immediately
   - **Blue LED turns ON + Continuous beep for 2 seconds** (indicates medicine taken)
   - Clear confirmation message displayed
   - System asks: "Measure vitals now?"

4. If button pressed within 5 seconds (for vitals):
   - Measures temperature and heart rate
   - Saves medication log with vital signs
   - Example log:
     ```
     ✓ MEDICATION LOGGED
     Medication: Aspirin
     Scheduled: 08:00 | Actual: 08:15:32
     Status: TAKEN
     
     📊 Vital Signs:
        • Temperature: 36.7°C
        • Heart Rate: 72 bpm
     ```

5. If no button press (5 seconds - skip vitals):
   - Saves medication log without vital signs
   - Status: "taken"
   - Alarm monitoring continues automatically

6. If no button press (60 seconds - missed):
   - Medication marked as "missed"
   - Logged without vital signs
   - Alarm monitoring continues automatically

**Health Monitoring (Only when Option 7 is active):**
- Checks temperature and heart rate every 10 seconds
- **Temperature abnormal** (< 18°C or > 30°C):
  - Red LED (near temp sensor) blinks
  - Buzzer sounds for 5 seconds
  - Console alert: `⚠️ ALERT: Abnormal Temperature: XX.X°C`

- **Heart rate abnormal** (< 60 bpm or > 120 bpm):
  - Green LED (near heart sensor) blinks
  - Buzzer sounds for 5 seconds
  - Console alert: `⚠️ ALERT: Abnormal Heart Rate: XX bpm`

- **Normal readings**:
  - Console display: `📊 Vitals: Temp=XX.X°C, HR=XX bpm`

- **Dashboard Updates:**
  - Shows active medications and their status
  - Displays upcoming medications with countdown
  - Updates every 30 seconds

**Stop Monitoring:**
- Press `Ctrl+C` to stop health monitoring
- Medication alarms continue running independently
- Or select option 8 (Exit) to stop everything

### Option 8: Exit

- Stops all monitoring (health monitoring + alarm monitoring)
- Turns off all LEDs and buzzer
- Closes database connections
- Cleans up GPIO
- Exits gracefully

---

## System Architecture

### Independent Alarm System ⭐ NEW

The medication alarm system runs **automatically** when the program starts:
- **No user action required** - Alarms work immediately
- **Background thread** - Runs independently of menu options
- **High accuracy** - Checks every 5 seconds with 30-second time window
- **Always active** - Works even when "Start Monitoring" is not active

### Health Monitoring System

The health monitoring system is **optional** and only active when Option 7 is selected:
- **Separate from alarms** - Does not affect medication alarms
- **Vitals only** - Monitors temperature and heart rate
- **Dashboard display** - Shows medication schedule and countdown
- **Can be stopped** - Press Ctrl+C to stop (alarms continue)

---

## Technical Specifications

### Sensor Specifications

**DS18B20 Temperature Sensor**
- **Measurement Range**: -55°C to +125°C
- **Accuracy**: ±0.5°C (in range 10°C to 85°C)
- **Resolution**: 9 to 12 bits (programmable)
- **Interface**: 1-Wire (single data line)
- **Power**: 3.0V to 5.5V
- **Current**: < 1.5mA active, < 750µA idle

**MAX30102 Heart Rate Sensor**
- **Measurement**: Heart rate (BPM), SpO2
- **Heart Rate Range**: 50-150 bpm (typical)
- **Interface**: I2C (SDA, SCL)
- **Power**: 3.3V or 5V (module dependent)
- **Sampling Rate**: Programmable (typically 50-3200 Hz)

### Threshold Values

- **Temperature Normal Range**: 18°C to 30°C
- **Heart Rate Normal Range**: 60 bpm to 120 bpm

**Note:** These thresholds are for demonstration. Real medical thresholds may differ.

### Database Schema

**Table: medications**
```sql
CREATE TABLE medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    schedule_time TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Table: medication_logs**
```sql
CREATE TABLE medication_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medication_id INTEGER,
    medication_name TEXT,
    scheduled_time TEXT,
    actual_time TEXT,
    status TEXT,
    temperature REAL,
    heart_rate INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medication_id) REFERENCES medications(id)
);
```

**Table: vitals_logs**
```sql
CREATE TABLE vitals_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    heart_rate INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### GPIO Pin Configuration

- **Mode**: BOARD (Physical pin numbering)
- **Pull-up**: Enabled on button pin (GPIO 27)
- **PWM**: Not used (digital I/O only)

---

## Safety & Medical Disclaimer

### ⚠️ IMPORTANT DISCLAIMER

**This system is designed for EDUCATIONAL and PERSONAL HEALTH AWARENESS purposes ONLY.**

- **NOT a medical device**: This system does NOT provide medical diagnosis or treatment
- **NOT FDA approved**: Not intended for clinical use
- **For educational purposes**: Demonstrates Health Informatics concepts
- **Consult healthcare professionals**: Always seek medical advice from qualified professionals
- **No liability**: Use at your own risk

### Intended Use

- Personal health awareness and monitoring
- Educational demonstration of Health Informatics systems
- Medication adherence tracking (non-medical)
- Basic vital signs observation

### Limitations

- Sensor accuracy may vary
- Not calibrated for medical use
- Thresholds are for demonstration only
- No medical interpretation provided
- No emergency response capabilities

---

## Troubleshooting

### Sensors Not Detected

**DS18B20 (Temperature):**
```bash
# Check 1-Wire interface
ls /sys/bus/w1/devices/

# If empty, enable 1-Wire:
sudo raspi-config
# Interface Options → 1-Wire → Enable

# Check wiring (Physical Pin 7)
```

**MAX30102 (Heart Rate):**
```bash
# Check I2C interface
sudo i2cdetect -y 1

# Should show device address (typically 0x57)
# If empty, enable I2C:
sudo raspi-config
# Interface Options → I2C → Enable

# Check wiring (Physical Pins 3 and 5)
```

### LEDs Not Working

- **Check polarity**: LED anode (+) must connect to GPIO pin
- **Verify resistor**: 220Ω resistor in series
- **Test with multimeter**: Check voltage at LED anode
- **Check GPIO pin**: Verify correct physical pin number

### Buzzer Not Working

- **Check buzzer type**: Active buzzer (not passive)
- **Verify voltage**: 5V active buzzer recommended
- **Check connections**: Positive to Pin 11, Negative to GND
- **Test directly**: Connect to 5V to verify buzzer works

### Button Not Responding

- **Check pull-up**: Code uses internal pull-up (GPIO.PUD_UP)
- **Verify connection**: Button connects GPIO to GND when pressed
- **Test continuity**: Use multimeter to check button
- **Debounce**: Code includes 0.1s debounce delay

### System Crashes or Freezes

- **Check power supply**: Ensure adequate 5V/2A power supply
- **Check connections**: Loose wires can cause issues
- **Review logs**: Check for error messages
- **Restart system**: `sudo reboot`

### View Medications/History Not Showing

- **Check database**: Verify `medhealth.db` file exists in the same directory
- **Check permissions**: Ensure write/read permissions for the database file
- **Press Enter**: Functions now pause and wait for Enter key - make sure to press Enter after viewing
- **Check console**: Output should be visible in terminal window
- **Error messages**: Any errors will be displayed with details - check for error messages
- **Empty database**: If no medications exist, appropriate message will be shown

### Medication Alarm Not Playing

- **Alarms run automatically** - No need to start monitoring (Option 7) for alarms to work
- **Check time format**: Verify medication schedule time matches current time (HH:MM format, e.g., 08:00)
- **Time window**: Alarms trigger within 30 seconds of scheduled time (before or after)
- **Check GPIO**: Verify buzzer and LED connections (Physical Pin 11 for buzzer, Pin 18 for Blue LED)
- **Test alarm**: Use Option 6 → Option 1 (Test Alarm) to verify hardware is working
- **Test button**: Use Option 6 → Option 2 (Test Button) to verify button works
- **Check button**: Verify button is connected correctly (Physical Pin 13)
- **System startup**: Alarms start automatically when program runs (check initialization messages)

### Database Errors

- **Check permissions**: Ensure write permissions in directory
- **Check disk space**: `df -h`
- **Verify file**: Check if `medhealth.db` exists
- **Recreate database**: Delete `medhealth.db` and restart

### Import Errors

```bash
# Reinstall dependencies
pip3 install --upgrade -r requirements.txt

# For RPi.GPIO:
sudo apt-get install python3-rpi.gpio

# For sensor libraries:
pip3 install --upgrade adafruit-circuitpython-max30102
pip3 install --upgrade w1thermsensor
```

---

## System Confirmation Checklist

### ✅ Heart Rate Measurement
- [ ] System measures heart rate in **BPM** (beats per minute)
- [ ] MAX30102 sensor connected and detected
- [ ] Heart rate displayed in console and logs

### ✅ Temperature Sensor
- [ ] DS18B20 temperature sensor connected
- [ ] Temperature measured in **°C** (Celsius)
- [ ] Temperature displayed in console and logs

### ✅ Buzzer Functionality
- [ ] One buzzer handles all alerts:
  - [ ] Medication reminders
  - [ ] Temperature abnormalities
  - [ ] Heart rate abnormalities
- [ ] Buzzer sounds correctly for each alert type

### ✅ LED Indicators
- [ ] **Green LED** near heart sensor blinks when HR abnormal
- [ ] **Red LED** near temp sensor blinks when temp abnormal
- [ ] **Blue LED** near button:
  - [ ] Blinks during medication alarm (with buzzer)
  - [ ] Turns ON for 2 seconds with continuous beep when medication taken (confirmation)

### ✅ Button Functionality
- [ ] Button turns off medication alarm
- [ ] Button confirms medication intake
- [ ] Button triggers 2-second continuous beep + Blue LED ON (confirmation indicator)

### ✅ Workflow Implementation
- [ ] Main menu with 8 options works correctly
- [ ] Medication alarm flow implemented as specified
- [ ] Manual vitals measurement works
- [ ] Continuous monitoring works
- [ ] History viewing works

---

## Conclusion

This Smart Medication Adherence and Health Monitoring System provides a complete solution for:

1. **Medication tracking** with smart alarms
2. **Vital signs monitoring** (temperature and heart rate in BPM)
3. **Health alerts** with visual and audio indicators
4. **Data logging** for personal health awareness

The system is designed as an educational Health Informatics tool, demonstrating how digital systems can support patient adherence and health awareness in a low-cost, practical manner.

---

**Document Version:** 3.0  
**Last Updated:** January 2024  
**Project:** Media Management - TH Deggendorf

**Recent Updates (v3.0):**
- ✅ **Independent Alarm System** - Alarms work automatically, no need to start monitoring
- ✅ **Improved Alarm Detection** - 5-second checks with 30-second time window for accuracy
- ✅ **PWM Buzzer Support** - Clear, audible tones with PWM (2000 Hz)
- ✅ **Enhanced Button Detection** - Better debouncing and real-time response
- ✅ **Button Test Function** - New test menu with button testing (Option 6 → Option 2)
- ✅ **Separated Monitoring** - Start Monitoring (Option 7) only does health monitoring
- ✅ **Better Alarm Timing** - Catches alarms even if check happens slightly before/after scheduled time
- ✅ **System Architecture** - Alarms run in background thread, always active
- ✅ All previous fixes from v2.2 (wiring, bug fixes, error handling)

---

## Quick Reference Card

### Pin Connections (Physical Pins)
- **DS18B20 DATA**: Pin 7
- **MAX30102 SDA**: Pin 3
- **MAX30102 SCL**: Pin 5
- **Buzzer**: Pin 11
- **Button**: Pin 13
- **LED Heart**: Pin 15
- **LED Temp**: Pin 16
- **LED Button**: Pin 18
- **5V**: Pin 2
- **GND**: Pin 6

### Key Commands
```bash
# Enable interfaces
sudo raspi-config

# Check I2C
sudo i2cdetect -y 1

# Check 1-Wire
ls /sys/bus/w1/devices/

# Run system
sudo python3 medhealth_system.py
```

### Normal Ranges
- **Temperature**: 18°C - 30°C
- **Heart Rate**: 60 - 120 bpm

---

**End of Documentation**

