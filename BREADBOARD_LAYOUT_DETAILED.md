# Detailed Breadboard Layout - 64 Rows, 5 Columns (A-E)

## Breadboard Structure

Your breadboard has:
- **64 rows** (numbered 1-64)
- **5 columns** per side (A, B, C, D, E)
- **Power rails** on left and right sides (Red = +, Black/Blue = -)
- **Center gap** separating left and right sections

## Component Placement Map

### Visual Layout

```
┌─────────────────────────────────────────────────────────────┐
│  POWER RAIL + (Red)    │  MAIN AREA (Rows 1-64)  │  POWER RAIL + │
│  POWER RAIL - (Black)  │  Columns A-E (each side) │  POWER RAIL - │
└─────────────────────────────────────────────────────────────┘
```

### Exact Component Positions

#### **POWER RAILS (Left Side)**
- **Red Rail (+)**: Connect to Physical Pin 2 (5V)
- **Black Rail (-)**: Connect to Physical Pin 6 (GND)

#### **ROW 1: DS18B20 Temperature Sensor**
```
Row 1:  [A] VDD (Red) ────→ Power Rail +
        [B] (empty)
        [C] DATA (Yellow) ─→ Physical Pin 7 (GPIO 4)
        [D] (empty)
        [E] GND (Black) ───→ Power Rail -
```

#### **ROW 2: 4.7kΩ Pull-up Resistor for DS18B20**
```
Row 2:  [A] 4.7kΩ Resistor (end 1)
        [B] 4.7kΩ Resistor (end 2) ─→ Power Rail +
        [C] Jumper wire ───────────→ Row 1-C (DATA line)
        [D] (empty)
        [E] (empty)
```

#### **ROW 6: MAX30102 Heart Rate Sensor**
```
Row 6:  [A] VIN ───────────→ Physical Pin 1 (3.3V) or Pin 2 (5V)
        [B] GND ───────────→ Power Rail -
        [C] SDA ───────────→ Physical Pin 3 (GPIO 2 / SDA)
        [D] SCL ───────────→ Physical Pin 5 (GPIO 3 / SCL)
        [E] (other pins if module has more)
```

#### **ROW 11: 220Ω Resistor for Green LED**
```
Row 11: [A] 220Ω Resistor (end 1) ─→ Physical Pin 15 (GPIO 22)
        [B] 220Ω Resistor (end 2)
        [C] (empty)
        [D] (empty)
        [E] (empty)
```

#### **ROW 12: Green LED (Heart Sensor)**
```
Row 12: [A] Green LED Anode (+) ─→ Jumper wire to Row 11-B
        [B] (empty)
        [C] (empty)
        [D] (empty)
        [E] Green LED Cathode (-) ─→ Power Rail -
```

#### **ROW 16: 220Ω Resistor for Red LED**
```
Row 16: [A] 220Ω Resistor (end 1) ─→ Physical Pin 16 (GPIO 23)
        [B] 220Ω Resistor (end 2)
        [C] (empty)
        [D] (empty)
        [E] (empty)
```

#### **ROW 17: Red LED (Temperature Sensor)**
```
Row 17: [A] Red LED Anode (+) ─→ Jumper wire to Row 16-B
        [B] (empty)
        [C] (empty)
        [D] (empty)
        [E] Red LED Cathode (-) ─→ Power Rail -
```

#### **ROW 21: 220Ω Resistor for Yellow LED**
```
Row 21: [A] 220Ω Resistor (end 1) ─→ Physical Pin 18 (GPIO 24)
        [B] 220Ω Resistor (end 2)
        [C] (empty)
        [D] (empty)
        [E] (empty)
```

#### **ROW 22: Yellow/Blue LED (Button)**
```
Row 22: [A] Yellow LED Anode (+) ─→ Jumper wire to Row 21-B
        [B] (empty)
        [C] (empty)
        [D] (empty)
        [E] Yellow LED Cathode (-) ─→ Power Rail -
```

#### **ROW 26: Push Button**
```
Row 26: [A] Button Terminal 1 ─→ Physical Pin 13 (GPIO 27)
        [B] Button Terminal 1 (same row, connected)
        [C] (empty)
        [D] Button Terminal 2 (same row, connected)
        [E] Button Terminal 2 ─→ Power Rail -
```

#### **ROW 31: Buzzer**
```
Row 31: [A] Buzzer Positive (+) ─→ Physical Pin 11 (GPIO 17)
        [B] (optional: 220Ω resistor for protection)
        [C] (empty)
        [D] (empty)
        [E] Buzzer Negative (-) ─→ Power Rail -
```

## Connection Summary Table

| Component | Row | Column | Connection To |
|-----------|-----|--------|---------------|
| DS18B20 VDD | 1 | A | Power Rail + |
| DS18B20 DATA | 1 | C | Physical Pin 7 |
| DS18B20 GND | 1 | E | Power Rail - |
| 4.7kΩ Resistor | 2 | A-B | Between DATA and VDD |
| MAX30102 VIN | 6 | A | Physical Pin 1 or 2 |
| MAX30102 GND | 6 | B | Power Rail - |
| MAX30102 SDA | 6 | C | Physical Pin 3 |
| MAX30102 SCL | 6 | D | Physical Pin 5 |
| Green LED Resistor | 11 | A-B | Pin 15 to LED |
| Green LED | 12 | A, E | Anode to Row 11-B, Cathode to GND |
| Red LED Resistor | 16 | A-B | Pin 16 to LED |
| Red LED | 17 | A, E | Anode to Row 16-B, Cathode to GND |
| Yellow LED Resistor | 21 | A-B | Pin 18 to LED |
| Yellow LED | 22 | A, E | Anode to Row 21-B, Cathode to GND |
| Button | 26 | A, E | Terminal 1 to Pin 13, Terminal 2 to GND |
| Buzzer | 31 | A, E | Positive to Pin 11, Negative to GND |

## Wiring Checklist

### Power Connections
- [ ] Physical Pin 2 (5V) → Power Rail +
- [ ] Physical Pin 6 (GND) → Power Rail -

### DS18B20 (Rows 1-2)
- [ ] Row 1-A: VDD → Power Rail +
- [ ] Row 1-C: DATA → Physical Pin 7
- [ ] Row 1-E: GND → Power Rail -
- [ ] Row 2: 4.7kΩ resistor between DATA and VDD

### MAX30102 (Row 6)
- [ ] Row 6-A: VIN → Physical Pin 1 or 2
- [ ] Row 6-B: GND → Power Rail -
- [ ] Row 6-C: SDA → Physical Pin 3
- [ ] Row 6-D: SCL → Physical Pin 5

### Green LED (Rows 11-12)
- [ ] Row 11-A: Resistor → Physical Pin 15
- [ ] Row 11-B: Resistor output
- [ ] Row 12-A: LED Anode → Row 11-B
- [ ] Row 12-E: LED Cathode → Power Rail -

### Red LED (Rows 16-17)
- [ ] Row 16-A: Resistor → Physical Pin 16
- [ ] Row 16-B: Resistor output
- [ ] Row 17-A: LED Anode → Row 16-B
- [ ] Row 17-E: LED Cathode → Power Rail -

### Yellow LED (Rows 21-22)
- [ ] Row 21-A: Resistor → Physical Pin 18
- [ ] Row 21-B: Resistor output
- [ ] Row 22-A: LED Anode → Row 21-B
- [ ] Row 22-E: LED Cathode → Power Rail -

### Button (Row 26)
- [ ] Row 26-A: Terminal 1 → Physical Pin 13
- [ ] Row 26-E: Terminal 2 → Power Rail -

### Buzzer (Row 31)
- [ ] Row 31-A: Positive → Physical Pin 11
- [ ] Row 31-E: Negative → Power Rail -

## Tips for Wiring

1. **Use Different Colored Jumper Wires**:
   - Red for 5V connections
   - Black for GND connections
   - Yellow/Green for GPIO signals
   - Other colors for component connections

2. **Keep Components Organized**:
   - Group related components together
   - Leave space between groups
   - Use rows 36-64 for future expansion

3. **Double-Check Connections**:
   - Verify all power connections
   - Check resistor values (220Ω for LEDs, 4.7kΩ for DS18B20)
   - Ensure LED polarity is correct (anode = +, cathode = -)

4. **Test Each Component**:
   - Test LEDs individually
   - Test button response
   - Test buzzer
   - Test sensors after wiring

## Troubleshooting

- **LED not working**: Check polarity and resistor connection
- **Button not responding**: Verify both terminals are connected correctly
- **Sensor not detected**: Verify I2C/1-Wire connections and enable interfaces
- **Buzzer not working**: Check polarity and pin connection

---

**Layout Version**: 2.0 (64-Row Breadboard)  
**Last Updated**: January 2024

