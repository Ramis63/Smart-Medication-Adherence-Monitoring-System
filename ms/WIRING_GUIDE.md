# Wiring Guide - Smart Medication Adherence System
## Raspberry Pi 3 Physical Pin Connections

### Component List
1. **DS18B20 Temperature Sensor** (1-wire)
2. **MAX30102 Heart Rate Sensor** (I2C)
3. **Buzzer** (Active/Passive)
4. **LEDs** (3x - Red, Green, Yellow/Blue)
5. **Button** (Push button with pull-up)
6. **Resistors** (220Ω for LEDs, 4.7kΩ for DS18B20, 10kΩ for button pull-up)

---

## Pin Connections (Physical Pin Numbers)

### Power Supply
- **Physical Pin 2** (5V) → VCC for sensors, buzzer, LEDs
- **Physical Pin 6** (GND) → Common Ground (connect all GNDs here)

### DS18B20 Temperature Sensor
- **VDD (Red wire)** → Physical Pin 2 (5V)
- **GND (Black wire)** → Physical Pin 6 (GND)
- **DATA (Yellow/White wire)** → Physical Pin 7 (GPIO 4)
- **4.7kΩ Resistor** → Between DATA and VDD (pull-up resistor)

### MAX30102 Heart Rate Sensor (I2C)
- **VIN** → Physical Pin 1 (3.3V) or Physical Pin 2 (5V) - check sensor specs
- **GND** → Physical Pin 6 (GND)
- **SDA** → Physical Pin 3 (GPIO 2 / SDA)
- **SCL** → Physical Pin 5 (GPIO 3 / SCL)

### Buzzer
- **Positive (+)** → Physical Pin 11 (GPIO 17) via 220Ω resistor (optional)
- **Negative (-)** → Physical Pin 6 (GND)

### LEDs
1. **LED for Heart Sensor** (Green LED - near MAX30102)
   - **Anode (+)** → Physical Pin 15 (GPIO 22) via 220Ω resistor
   - **Cathode (-)** → Physical Pin 6 (GND)

2. **LED for Temperature Sensor** (Red LED - near DS18B20)
   - **Anode (+)** → Physical Pin 16 (GPIO 23) via 220Ω resistor
   - **Cathode (-)** → Physical Pin 6 (GND)

3. **LED for Button** (Yellow/Blue LED - near button)
   - **Anode (+)** → Physical Pin 18 (GPIO 24) via 220Ω resistor
   - **Cathode (-)** → Physical Pin 6 (GND)

### Button
- **One terminal** → Physical Pin 13 (GPIO 27)
- **Other terminal** → Physical Pin 6 (GND)
- **Note:** Code uses internal pull-up, so button connects GPIO to GND when pressed

---

## Breadboard Layout (64 Rows, 5 Columns A-E)

### Standard Breadboard Structure
- **Power Rails**: Left and right sides (Red = +, Blue/Black = -)
- **Main Area**: Rows 1-64, Columns A-E (left side) and A-E (right side)
- **Center Gap**: Separates left and right sections (for DIP ICs)

### Recommended Component Placement

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
    ┌─────────────────────────────────────────────────────────────┐
    │                    BREADBOARD (64 Rows, A-E)                 │
    │                                                               │
    │  LEFT POWER RAIL (+)  │  MAIN AREA  │  RIGHT POWER RAIL (+)  │
    │  LEFT POWER RAIL (-)  │             │  RIGHT POWER RAIL (-)   │
    │                                                               │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ POWER RAIL + (Red) ← Pin 2 (5V)                     │    │
    │  │ POWER RAIL - (Black) ← Pin 6 (GND)                   │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 1-5:   DS18B20 Temperature Sensor                       │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 1:  [A] VDD (Red) → Power Rail +                  │    │
    │  │         [B] (empty)                                    │    │
    │  │         [C] DATA (Yellow) → Pin 7 (GPIO4)            │    │
    │  │         [D] (empty)                                    │    │
    │  │         [E] GND (Black) → Power Rail -               │    │
    │  │                                                         │    │
    │  │ Row 2:  [A] 4.7kΩ Resistor (one end)                  │    │
    │  │         [B] 4.7kΩ Resistor (other end) → Power Rail + │    │
    │  │         [C] 4.7kΩ Resistor (connected to Row 1-C)     │    │
    │  │         [D] (empty)                                    │    │
    │  │         [E] (empty)                                    │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 6-10:  MAX30102 Heart Rate Sensor Module                 │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 6:  [A] VIN → Pin 1 (3.3V) or Pin 2 (5V)        │    │
    │  │         [B] GND → Power Rail -                       │    │
    │  │         [C] SDA → Pin 3 (GPIO 2 / SDA)               │    │
    │  │         [D] SCL → Pin 5 (GPIO 3 / SCL)               │    │
    │  │         [E] (other pins if needed)                    │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 11-15: Green LED (Heart Sensor) + Resistor              │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 11: [A] 220Ω Resistor → Pin 15 (GPIO 22)        │    │
    │  │         [B] 220Ω Resistor (other end)                │    │
    │  │         [C] (empty)                                  │    │
    │  │         [D] (empty)                                  │    │
    │  │         [E] (empty)                                  │    │
    │  │                                                       │    │
    │  │ Row 12: [A] Green LED Anode (+) → Row 11-B          │    │
    │  │         [B] (empty)                                  │    │
    │  │         [C] (empty)                                  │    │
    │  │         [D] (empty)                                  │    │
    │  │         [E] Green LED Cathode (-) → Power Rail -    │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 16-20: Red LED (Temperature Sensor) + Resistor          │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 16: [A] 220Ω Resistor → Pin 16 (GPIO 23)        │    │
    │  │         [B] 220Ω Resistor (other end)              │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] (empty)                                │    │
    │  │         [E] (empty)                                │    │
    │  │                                                     │    │
    │  │ Row 17: [A] Red LED Anode (+) → Row 16-B          │    │
    │  │         [B] (empty)                                │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] (empty)                                │    │
    │  │         [E] Red LED Cathode (-) → Power Rail -    │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 21-25: Yellow/Blue LED (Button) + Resistor               │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 21: [A] 220Ω Resistor → Pin 18 (GPIO 24)        │    │
    │  │         [B] 220Ω Resistor (other end)              │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] (empty)                                │    │
    │  │         [E] (empty)                                │    │
    │  │                                                     │    │
    │  │ Row 22: [A] Yellow LED Anode (+) → Row 21-B        │    │
    │  │         [B] (empty)                                │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] (empty)                                │    │
    │  │         [E] Yellow LED Cathode (-) → Power Rail -  │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 26-30: Push Button                                       │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 26: [A] Button Terminal 1 → Pin 13 (GPIO 27)    │    │
    │  │         [B] Button Terminal 1 (same row)          │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] Button Terminal 2 (same row)          │    │
    │  │         [E] Button Terminal 2 → Power Rail -      │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 31-35: Buzzer                                           │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │ Row 31: [A] Buzzer Positive (+) → Pin 11 (GPIO 17)  │    │
    │  │         [B] (optional: 220Ω resistor in series)      │    │
    │  │         [C] (empty)                                │    │
    │  │         [D] (empty)                                │    │
    │  │         [E] Buzzer Negative (-) → Power Rail -     │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                               │
    │  ROW 36-64: Available for future expansion                   │
    │                                                               │
    └─────────────────────────────────────────────────────────────┘
```

### Detailed Row-by-Row Placement Guide

| Row Range | Component | Column Positions |
|-----------|-----------|-----------------|
| **Power Rails** | Left/Right sides | Red (+) and Black (-) rails |
| **Row 1** | DS18B20 Sensor | A: VDD, C: DATA, E: GND |
| **Row 2** | 4.7kΩ Resistor | A-B: Resistor (DATA to VDD pull-up) |
| **Row 6** | MAX30102 Module | A: VIN, B: GND, C: SDA, D: SCL |
| **Row 11** | 220Ω Resistor (Green LED) | A-B: Resistor |
| **Row 12** | Green LED | A: Anode, E: Cathode |
| **Row 16** | 220Ω Resistor (Red LED) | A-B: Resistor |
| **Row 17** | Red LED | A: Anode, E: Cathode |
| **Row 21** | 220Ω Resistor (Yellow LED) | A-B: Resistor |
| **Row 22** | Yellow/Blue LED | A: Anode, E: Cathode |
| **Row 26** | Push Button | A-B: Terminal 1, D-E: Terminal 2 |
| **Row 31** | Buzzer | A: Positive (+), E: Negative (-) |

---

## Detailed Connection Steps

### Step 1: Power Connections
1. Connect **Physical Pin 2 (5V)** to **LEFT power rail (+)**
2. Connect **Physical Pin 6 (GND)** to **LEFT power rail (-)**
3. **Optional**: Connect left and right power rails together for easier wiring

### Step 2: DS18B20 Temperature Sensor (Rows 1-2)
1. **Row 1**: Place DS18B20 sensor pins:
   - **Column A**: VDD (Red wire) → Connect to power rail (+)
   - **Column C**: DATA (Yellow wire) → Connect to **Physical Pin 7 (GPIO 4)**
   - **Column E**: GND (Black wire) → Connect to power rail (-)

2. **Row 2**: Place 4.7kΩ pull-up resistor:
   - **Column A**: One end of resistor
   - **Column B**: Other end of resistor → Connect to power rail (+)
   - **Column C**: Connect to Row 1-C (DATA line) using jumper wire

### Step 3: MAX30102 Heart Rate Sensor (Row 6)
1. **Row 6**: Place MAX30102 module pins:
   - **Column A**: VIN → Connect to **Physical Pin 1 (3.3V)** or **Pin 2 (5V)**
   - **Column B**: GND → Connect to power rail (-)
   - **Column C**: SDA → Connect to **Physical Pin 3 (GPIO 2 / SDA)**
   - **Column D**: SCL → Connect to **Physical Pin 5 (GPIO 3 / SCL)**

### Step 4: Green LED - Heart Sensor (Rows 11-12)
1. **Row 11**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 15 (GPIO 22)**
   - **Column B**: Other end (resistor output)

2. **Row 12**: Place Green LED:
   - **Column A**: Anode (+) → Connect to Row 11-B (via jumper wire)
   - **Column E**: Cathode (-) → Connect to power rail (-)

### Step 5: Red LED - Temperature Sensor (Rows 16-17)
1. **Row 16**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 16 (GPIO 23)**
   - **Column B**: Other end (resistor output)

2. **Row 17**: Place Red LED:
   - **Column A**: Anode (+) → Connect to Row 16-B (via jumper wire)
   - **Column E**: Cathode (-) → Connect to power rail (-)

### Step 6: Yellow/Blue LED - Button (Rows 21-22)
1. **Row 21**: Place 220Ω resistor:
   - **Column A**: One end → Connect to **Physical Pin 18 (GPIO 24)**
   - **Column B**: Other end (resistor output)

2. **Row 22**: Place Yellow/Blue LED:
   - **Column A**: Anode (+) → Connect to Row 21-B (via jumper wire)
   - **Column E**: Cathode (-) → Connect to power rail (-)

### Step 7: Push Button (Row 26)
1. **Row 26**: Place push button:
   - **Column A-B**: Button Terminal 1 (same row, connected internally)
   - **Column D-E**: Button Terminal 2 (same row, connected internally)
   - Connect **Column A** to **Physical Pin 13 (GPIO 27)**
   - Connect **Column E** to power rail (-)
   - **Note:** Internal pull-up is enabled in code, so button pulls GPIO LOW when pressed

### Step 8: Buzzer (Row 31)
1. **Row 31**: Place buzzer:
   - **Column A**: Positive (+) terminal → Connect to **Physical Pin 11 (GPIO 17)**
   - **Optional**: Add 220Ω resistor between Column A and buzzer for protection
   - **Column E**: Negative (-) terminal → Connect to power rail (-)

### Wiring Tips:
- Use jumper wires to connect components on the same row
- All GND connections go to power rail (-)
- Keep components organized by rows for easier troubleshooting
- Leave space between component groups for clarity

---

## Pin Summary Table

| Component | Physical Pin | GPIO Pin | Function |
|-----------|--------------|----------|----------|
| DS18B20 DATA | 7 | GPIO 4 | 1-Wire Data |
| MAX30102 SDA | 3 | GPIO 2 | I2C Data |
| MAX30102 SCL | 5 | GPIO 3 | I2C Clock |
| Buzzer | 11 | GPIO 17 | Output |
| Button | 13 | GPIO 27 | Input (Pull-up) |
| LED Heart | 15 | GPIO 22 | Output |
| LED Temp | 16 | GPIO 23 | Output |
| LED Button | 18 | GPIO 24 | Output |
| 5V Power | 2 | - | Power |
| 3.3V Power | 1 | - | Power (for MAX30102) |
| GND | 6 | - | Ground |

---

## Safety Notes

1. **Double-check all connections** before powering on
2. **Use appropriate resistors** to protect LEDs and GPIO pins
3. **Verify sensor voltage requirements** (3.3V vs 5V)
4. **Test each component individually** before full system test
5. **Ensure proper grounding** - all GND connections must be connected

---

## Testing Connections

After wiring, test each component:

1. **LEDs**: Run `test_alarm()` function - all LEDs should blink
2. **Buzzer**: Run `test_alarm()` function - buzzer should sound
3. **Button**: Press button and check if system responds
4. **Temperature**: Use option 4 (Measure Vitals) - should read temperature
5. **Heart Rate**: Use option 4 (Measure Vitals) - should read heart rate

---

## Troubleshooting

- **LEDs not working**: Check resistor values and polarity
- **Buzzer not working**: Verify pin connection and buzzer type (active vs passive)
- **Sensors not detected**: Check I2C/1-Wire connections and enable interfaces
- **Button not responding**: Verify pull-up configuration and connections

