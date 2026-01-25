# CORRECTED Breadboard Wiring Guide
## Important: Breadboard Row Connections

**CRITICAL UNDERSTANDING:**
- In a breadboard, each **horizontal ROW** connects all columns (A, B, C, D, E) together
- Components in the **SAME ROW** are electrically connected
- You **CANNOT** put VDD and GND in the same row (short circuit!)
- You **CANNOT** put LED anode and cathode in the same row (short circuit!)

## Corrected Wiring Instructions

### DS18B20 Temperature Sensor
**Use SEPARATE rows for each pin:**

- **Row 1, Column A**: VDD wire → Connect to Power Rail (+)
- **Row 2, Column A**: DATA wire → Connect to Physical Pin 7 (GPIO 4)
- **Row 3, Column A**: GND wire → Connect to Power Rail (-)

**4.7kΩ Pull-up Resistor:**
- **Row 4, Column A**: One end of resistor
- **Row 4, Column B**: Other end → Connect to Power Rail (+)
- **Row 4, Column C**: Jumper wire to Row 2-A (DATA line)

### MAX30102 Heart Rate Sensor
**Use SEPARATE rows for each pin:**

- **Row 6, Column A**: VIN → Connect to Physical Pin 1 (3.3V) or Pin 2 (5V)
- **Row 7, Column A**: GND → Connect to Power Rail (-)
- **Row 8, Column A**: SDA → Connect to Physical Pin 3 (GPIO 2 / SDA)
- **Row 9, Column A**: SCL → Connect to Physical Pin 5 (GPIO 3 / SCL)

### Green LED (Heart Sensor) - Near MAX30102
**Use SEPARATE rows:**

- **Row 11, Column A**: 220Ω Resistor (one end) → Connect to Physical Pin 15 (GPIO 22)
- **Row 11, Column B**: 220Ω Resistor (other end)
- **Row 12, Column A**: Green LED Anode (+) → Jumper wire to Row 11-B
- **Row 13, Column A**: Green LED Cathode (-) → Connect to Power Rail (-)

### Red LED (Temperature Sensor) - Near DS18B20
**Use SEPARATE rows:**

- **Row 16, Column A**: 220Ω Resistor (one end) → Connect to Physical Pin 16 (GPIO 23)
- **Row 16, Column B**: 220Ω Resistor (other end)
- **Row 17, Column A**: Red LED Anode (+) → Jumper wire to Row 16-B
- **Row 18, Column A**: Red LED Cathode (-) → Connect to Power Rail (-)

### Blue LED (Button) - Near Button
**Use SEPARATE rows:**

- **Row 21, Column A**: 220Ω Resistor (one end) → Connect to Physical Pin 18 (GPIO 24)
- **Row 21, Column B**: 220Ω Resistor (other end)
- **Row 22, Column A**: Blue LED Anode (+) → Jumper wire to Row 21-B
- **Row 23, Column A**: Blue LED Cathode (-) → Connect to Power Rail (-)

### Push Button (Row 26)
**Button terminals can be in same row (button connects them when pressed):**

- **Row 26, Column A-B**: Button Terminal 1 → Connect to Physical Pin 13 (GPIO 27)
- **Row 26, Column D-E**: Button Terminal 2 → Connect to Power Rail (-)

### Buzzer (Row 31)
**Use SEPARATE rows:**

- **Row 31, Column A**: Buzzer Positive (+) → Connect to Physical Pin 11 (GPIO 17)
- **Row 32, Column A**: Buzzer Negative (-) → Connect to Power Rail (-)

---

## Summary of Corrected Row Layout

| Row | Component | Connection |
|-----|-----------|------------|
| 1 | DS18B20 VDD | Power Rail + |
| 2 | DS18B20 DATA | Pin 7 (GPIO 4) |
| 3 | DS18B20 GND | Power Rail - |
| 4 | 4.7kΩ Resistor | DATA to VDD pull-up |
| 6 | MAX30102 VIN | Pin 1/2 (3.3V/5V) |
| 7 | MAX30102 GND | Power Rail - |
| 8 | MAX30102 SDA | Pin 3 (GPIO 2) |
| 9 | MAX30102 SCL | Pin 5 (GPIO 3) |
| 11 | 220Ω Resistor (Green) | Pin 15 to LED |
| 12 | Green LED Anode | Row 11-B |
| 13 | Green LED Cathode | Power Rail - |
| 16 | 220Ω Resistor (Red) | Pin 16 to LED |
| 17 | Red LED Anode | Row 16-B |
| 18 | Red LED Cathode | Power Rail - |
| 21 | 220Ω Resistor (Blue) | Pin 18 to LED |
| 22 | Blue LED Anode | Row 21-B |
| 23 | Blue LED Cathode | Power Rail - |
| 26 | Button | Pin 13 to GND |
| 31 | Buzzer Positive | Pin 11 |
| 32 | Buzzer Negative | Power Rail - |

