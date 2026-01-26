#!/usr/bin/env python3
"""
Smart Medication Adherence and Health Monitoring System
Raspberry Pi 3 - Complete Implementation
"""

import sqlite3
import threading
import time
import datetime
import signal
import sys
from typing import Optional, Tuple, List
import json
import os
try:
    import select
except ImportError:
    # Windows doesn't have select module, use alternative
    select = None

# GPIO imports
try:
    import RPi.GPIO as GPIO
except ImportError:
    print("Warning: RPi.GPIO not available. Using mock mode.")
    GPIO = None

# Sensor imports
try:
    import board
    import busio
    import adafruit_max30102
    import adafruit_mlx90614
except ImportError:
    print("Warning: Sensor libraries not available. Using mock mode.")
    board = None
    busio = None
    adafruit_max30102 = None
    adafruit_mlx90614 = None

# For DS18B20 temperature sensor (1-wire)
try:
    from w1thermsensor import W1ThermSensor
except ImportError:
    W1ThermSensor = None

# Pin Definitions (Physical Pin Numbers on Raspberry Pi 3)
BUZZER_PIN = 11  # Physical Pin 11 (GPIO 17)
BUTTON_PIN = 13  # Physical Pin 13 (GPIO 27)
LED_HEART_PIN = 15  # Physical Pin 15 (GPIO 22) - Near heart sensor
LED_TEMP_PIN = 16  # Physical Pin 16 (GPIO 23) - Near temp sensor
LED_BUTTON_PIN = 18  # Physical Pin 18 (GPIO 24) - Near button

# Sensor thresholds
TEMP_MIN = 18.0  # °C
TEMP_MAX = 30.0  # °C
HR_MIN = 60  # bpm
HR_MAX = 120  # bpm

# Global variables
monitoring_active = False
alarm_active = False
system_running = True
heart_rate_sensor = None
temp_sensor = None
pwm_buzzer = None  # PWM object for buzzer
alarm_monitoring_active = False  # Independent alarm monitoring thread
alarm_monitoring_thread = None  # Thread for independent alarm monitoring
alarm_monitoring_active = False  # Independent alarm monitoring thread
alarm_monitoring_thread = None  # Thread for independent alarm monitoring

# Database setup
DB_FILE = "medhealth.db"

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Medications table
    c.execute('''CREATE TABLE IF NOT EXISTS medications
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  schedule_time TEXT NOT NULL,
                  active INTEGER DEFAULT 1,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Medication logs table
    c.execute('''CREATE TABLE IF NOT EXISTS medication_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  medication_id INTEGER,
                  medication_name TEXT,
                  scheduled_time TEXT,
                  actual_time TEXT,
                  status TEXT,
                  temperature REAL,
                  heart_rate INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (medication_id) REFERENCES medications(id))''')
    
    # Vitals logs table
    c.execute('''CREATE TABLE IF NOT EXISTS vitals_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  temperature REAL,
                  heart_rate INTEGER,
                  status TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def init_gpio():
    """Initialize GPIO pins and ensure all LEDs are OFF"""
    global pwm_buzzer
    
    if GPIO is None:
        return
    
    try:
        # First, clean up any previous GPIO state
        GPIO.cleanup()
        time.sleep(0.1)  # Small delay to ensure cleanup completes
    except:
        pass  # Ignore errors if GPIO wasn't initialized before
    
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setwarnings(False)
    
    # Setup outputs and immediately set to LOW (OFF state)
    # This ensures LEDs are OFF before they can turn on
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_HEART_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_TEMP_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_BUTTON_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    # Initialize PWM for buzzer (for better sound - works with both active and passive buzzers)
    # PWM frequency: 2000 Hz (audible tone)
    try:
        pwm_buzzer = GPIO.PWM(BUZZER_PIN, 2000)  # 2000 Hz frequency
        pwm_buzzer.start(0)  # Start with 0% duty cycle (off)
    except Exception as e:
        pwm_buzzer = None
        print(f"Note: Using digital mode for buzzer (PWM not available: {e})")
    
    # Explicitly set all outputs to LOW again (redundant but ensures state)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_HEART_PIN, GPIO.LOW)
    GPIO.output(LED_TEMP_PIN, GPIO.LOW)
    GPIO.output(LED_BUTTON_PIN, GPIO.LOW)
    
    # Setup input with pull-up resistor
    # Button connected: One terminal to GPIO pin, other to GND
    # When pressed: GPIO reads LOW, when not pressed: GPIO reads HIGH (pull-up)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Test button state on initialization
    button_state = GPIO.input(BUTTON_PIN)
    if button_state == GPIO.LOW:
        print("⚠️  Warning: Button appears to be pressed at startup (check wiring)")
    else:
        print("✓ Button initialized correctly (not pressed)")
    
    # One more explicit LOW to be absolutely sure
    time.sleep(0.05)  # Small delay
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_HEART_PIN, GPIO.LOW)
    GPIO.output(LED_TEMP_PIN, GPIO.LOW)
    GPIO.output(LED_BUTTON_PIN, GPIO.LOW)
    
    print("✓ GPIO initialized - All LEDs and buzzer set to OFF")

def init_sensors():
    """Initialize sensors"""
    global heart_rate_sensor, temp_sensor
    
    # Initialize DS18B20 temperature sensor
    try:
        if W1ThermSensor:
            temp_sensor = W1ThermSensor()
            print("✓ Temperature sensor (DS18B20) initialized")
        else:
            print("⚠ Temperature sensor library not available")
    except Exception as e:
        print(f"⚠ Temperature sensor error: {e}")
        temp_sensor = None
    
    # Initialize MAX30102 heart rate sensor
    try:
        if board and busio and adafruit_max30102:
            i2c = busio.I2C(board.SCL, board.SDA)
            heart_rate_sensor = adafruit_max30102.MAX30102(i2c)
            print("✓ Heart rate sensor (MAX30102) initialized")
        else:
            print("⚠ Heart rate sensor library not available")
    except Exception as e:
        print(f"⚠ Heart rate sensor error: {e}")
        heart_rate_sensor = None

def read_temperature() -> Optional[float]:
    """Read temperature from DS18B20 sensor"""
    if temp_sensor:
        try:
            temp = temp_sensor.get_temperature()
            return round(temp, 1)
        except Exception as e:
            print(f"Temperature read error: {e}")
            return None
    else:
        # Mock data for testing
        return round(36.5 + (time.time() % 10) * 0.1, 1)

def read_heart_rate() -> Optional[int]:
    """Read heart rate from MAX30102 sensor"""
    if heart_rate_sensor:
        try:
            # MAX30102 requires sampling over time
            samples = []
            start_time = time.time()
            timeout = 10  # seconds
            
            while time.time() - start_time < timeout:
                if heart_rate_sensor.ir > 10000:  # Valid reading
                    # Simple BPM calculation (in real implementation, use proper algorithm)
                    # This is a simplified version
                    red = heart_rate_sensor.red
                    if red > 0:
                        # Estimate BPM (simplified - real implementation needs peak detection)
                        bpm_estimate = int(60 + (red % 100))
                        samples.append(bpm_estimate)
                        if len(samples) >= 10:
                            break
                time.sleep(0.1)
            
            if samples:
                avg_bpm = int(sum(samples) / len(samples))
                return avg_bpm if 50 <= avg_bpm <= 150 else None
            return None
        except Exception as e:
            print(f"Heart rate read error: {e}")
            return None
    else:
        # Mock data for testing
        return int(70 + (time.time() % 20))

def buzzer_on():
    """Turn buzzer on - uses PWM if available, otherwise digital"""
    global pwm_buzzer
    if GPIO:
        if pwm_buzzer:
            try:
                pwm_buzzer.ChangeDutyCycle(50)  # 50% duty cycle for audible tone
            except:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)

def buzzer_off():
    """Turn buzzer off (ensure LOW state)"""
    global pwm_buzzer
    if GPIO:
        if pwm_buzzer:
            try:
                pwm_buzzer.ChangeDutyCycle(0)  # 0% duty cycle = off
            except:
                GPIO.output(BUZZER_PIN, GPIO.LOW)
        else:
            try:
                GPIO.output(BUZZER_PIN, GPIO.LOW)
            except:
                # If pin not initialized, initialize it now
                GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
                GPIO.output(BUZZER_PIN, GPIO.LOW)

def led_on(pin):
    """Turn LED on"""
    if GPIO:
        GPIO.output(pin, GPIO.HIGH)

def led_off(pin):
    """Turn LED off (ensure LOW state)"""
    if GPIO:
        try:
            GPIO.output(pin, GPIO.LOW)
        except:
            # If pin not initialized, initialize it now
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
            GPIO.output(pin, GPIO.LOW)

def blink_led(pin, duration=1.0, blink_rate=0.5):
    """Blink LED for specified duration"""
    if GPIO:
        end_time = time.time() + duration
        while time.time() < end_time:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(blink_rate)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(blink_rate)

def beep_buzzer(duration=0.5, frequency=0.01):
    """Beep buzzer for specified duration (beeping pattern)"""
    if GPIO:
        end_time = time.time() + duration
        while time.time() < end_time:
            buzzer_on()
            time.sleep(frequency)
            buzzer_off()
            time.sleep(frequency)

def continuous_beep(duration=2.0):
    """Continuous beep for specified duration (solid tone)"""
    if GPIO:
        buzzer_on()
        time.sleep(duration)
        buzzer_off()

def button_pressed() -> bool:
    """Check if button is pressed (with immediate check)"""
    if GPIO:
        try:
            # Button is LOW when pressed (pull-up configuration)
            state = GPIO.input(BUTTON_PIN)
            return state == GPIO.LOW
        except:
            return False
    return False

def wait_for_button(timeout=5) -> bool:
    """Wait for button press with timeout and improved debouncing"""
    if GPIO is None:
        return False
    
    start_time = time.time()
    button_was_pressed = False
    press_start_time = None
    debounce_time = 0.05  # 50ms debounce time
    
    while time.time() - start_time < timeout:
        current_state = button_pressed()
        
        if current_state:
            # Button is currently pressed
            if not button_was_pressed:
                # Button just got pressed - start debounce timer
                press_start_time = time.time()
                button_was_pressed = True
            else:
                # Button still pressed - check if debounce time has passed
                if press_start_time and (time.time() - press_start_time) >= debounce_time:
                    # Button has been pressed long enough - valid press
                    # Wait for release to confirm
                    time.sleep(0.05)
                    if not button_pressed():
                        return True
        else:
            # Button is not pressed - reset state
            button_was_pressed = False
            press_start_time = None
        
        time.sleep(0.02)  # Check every 20ms for responsiveness
    
    return False

def add_medication(name: str, schedule_time: str):
    """Add a new medication with confirmation"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO medications (name, schedule_time) VALUES (?, ?)",
              (name, schedule_time))
    conn.commit()
    med_id = c.lastrowid
    conn.close()
    
    print("\n" + "=" * 70)
    print("✓ MEDICATION ADDED SUCCESSFULLY")
    print("=" * 70)
    print(f"   ID: {med_id}")
    print(f"   Name: {name}")
    print(f"   Schedule Time: {schedule_time}")
    print("=" * 70)

def view_medications():
    """View all active medications with better formatting"""
    try:
        medications = get_active_medications()
        
        if not medications:
            print("\n📋 No active medications found.")
            input("\nPress Enter to continue...")
            return
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M")
        
        print("\n" + "=" * 70)
        print(" " * 20 + "📋 ACTIVE MEDICATIONS")
        print("=" * 70)
        print(f"\n📅 Date: {current_date}  |  🕐 Current Time: {current_time}")
        print("─" * 70)
        print(f"{'ID':<5} {'Medication Name':<25} {'Schedule Time':<15} {'Status':<20}")
        print("─" * 70)
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        for med_id, name, schedule_time in medications:
            # Check if taken today
            c.execute('''SELECT status, actual_time FROM medication_logs 
                         WHERE medication_id = ? AND DATE(created_at) = ? 
                         ORDER BY created_at DESC LIMIT 1''',
                      (med_id, current_date))
            result = c.fetchone()
            
            if result:
                status, actual_time = result
                if status == "taken":
                    status_display = f"✓ Taken at {actual_time}"
                else:
                    status_display = "✗ Missed"
            else:
                # Check if time has passed
                if schedule_time <= current_time:
                    status_display = "⏰ Pending"
                else:
                    status_display = "⏳ Upcoming"
            
            print(f"{med_id:<5} {name:<25} {schedule_time:<15} {status_display:<20}")
        
        conn.close()
        print("─" * 70)
        print(f"\nTotal Active Medications: {len(medications)}")
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\n❌ Error viewing medications: {e}")
        input("\nPress Enter to continue...")

def delete_medication(med_id: int):
    """Delete a medication with confirmation"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get medication info before deleting
    c.execute("SELECT name, schedule_time FROM medications WHERE id = ?", (med_id,))
    result = c.fetchone()
    
    if not result:
        print(f"\n❌ Error: Medication ID {med_id} not found.")
        conn.close()
        return
    
    name, schedule_time = result
    
    # Delete medication
    c.execute("UPDATE medications SET active = 0 WHERE id = ?", (med_id,))
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 70)
    print("🗑️  MEDICATION DELETED")
    print("=" * 70)
    print(f"   ID: {med_id}")
    print(f"   Name: {name}")
    print(f"   Schedule Time: {schedule_time}")
    print("\n   This medication will no longer trigger alarms.")
    print("=" * 70)

def measure_vitals_manual() -> Tuple[Optional[float], Optional[int]]:
    """Manual vitals measurement with improved display"""
    print("\n" + "=" * 70)
    print(" " * 20 + "📊 MANUAL VITALS MEASUREMENT")
    print("=" * 70)
    print("\n⏳ Please wait while sensors initialize...")
    time.sleep(1)
    
    # Measure temperature
    print("\n🌡️  Measuring Temperature...")
    temp = read_temperature()
    if temp:
        status = "✅ NORMAL" if TEMP_MIN <= temp <= TEMP_MAX else "⚠️  ABNORMAL"
        print(f"   Temperature: {temp}°C | Status: {status}")
        print(f"   Normal Range: {TEMP_MIN}°C - {TEMP_MAX}°C")
    else:
        print("   ❌ Error: Could not read temperature sensor")
    
    # Measure heart rate
    print("\n💓 Measuring Heart Rate...")
    print("   👆 Please place finger on heart rate sensor")
    print("   ⏳ Measuring (this may take up to 10 seconds)...")
    
    hr = read_heart_rate()
    if hr:
        status = "✅ NORMAL" if HR_MIN <= hr <= HR_MAX else "⚠️  ABNORMAL"
        print(f"   Heart Rate: {hr} bpm | Status: {status}")
        print(f"   Normal Range: {HR_MIN} - {HR_MAX} bpm")
    else:
        print("   ❌ Error: Could not read heart rate sensor")
        print("   💡 Tip: Ensure finger is properly placed on sensor")
    
    print("\n" + "=" * 70)
    
    return temp, hr

def log_medication(medication_id: int, medication_name: str, scheduled_time: str,
                  actual_time: str, status: str, temperature: Optional[float] = None,
                  heart_rate: Optional[int] = None):
    """Log medication intake with detailed information"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO medication_logs 
                 (medication_id, medication_name, scheduled_time, actual_time, status, temperature, heart_rate)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (medication_id, medication_name, scheduled_time, actual_time, status, temperature, heart_rate))
    conn.commit()
    conn.close()
    
    status_emoji = "✓" if status == "taken" else "✗"
    
    print("\n" + "=" * 70)
    print(f" {status_emoji} MEDICATION LOGGED")
    print("=" * 70)
    print(f"   Medication: {medication_name}")
    print(f"   Scheduled: {scheduled_time} | Actual: {actual_time}")
    print(f"   Status: {status.upper()}")
    
    if temperature or heart_rate:
        print(f"\n   📊 Vital Signs:")
        if temperature:
            print(f"      • Temperature: {temperature}°C")
        if heart_rate:
            print(f"      • Heart Rate: {heart_rate} bpm")
    else:
        print(f"\n   📊 Vital Signs: Not measured")
    
    print("=" * 70)

def view_history():
    """View medication history with improved formatting"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''SELECT medication_name, scheduled_time, actual_time, status, 
                     temperature, heart_rate, created_at
                     FROM medication_logs 
                     ORDER BY created_at DESC LIMIT 20''')
        logs = c.fetchall()
        conn.close()
        
        if not logs:
            print("\n📈 No medication history found.")
            input("\nPress Enter to continue...")
            return
        
        print("\n" + "=" * 85)
        print(" " * 20 + "📈 MEDICATION HISTORY")
        print(" " * 12 + "(Last 20 Entries)")
        print("=" * 85)
        print(f"{'Medication':<20} {'Scheduled':<12} {'Actual':<12} {'Status':<10} {'Vitals':<25} {'Date/Time':<20}")
        print("─" * 85)
        
        for name, sched_time, actual_time, status, temp, hr, created_at in logs:
            status_emoji = "✓" if status == "taken" else "✗"
            status_display = f"{status_emoji} {status.upper()}"
            
            # Format vitals
            vitals = ""
            if temp and hr:
                vitals = f"T:{temp}°C HR:{hr}bpm"
            elif temp:
                vitals = f"T:{temp}°C"
            elif hr:
                vitals = f"HR:{hr}bpm"
            else:
                vitals = "-"
            
            # Format date/time
            try:
                dt = datetime.datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                date_str = dt.strftime("%Y-%m-%d")
                time_str = dt.strftime("%H:%M:%S")
                datetime_display = f"{date_str} {time_str}"
            except:
                datetime_display = str(created_at)[:19] if created_at else "-"
            
            print(f"{name:<20} {sched_time:<12} {actual_time:<12} {status_display:<10} {vitals:<25} {datetime_display:<20}")
            print("─" * 85)
        
        print("=" * 85)
        
        # Statistics
        taken_count = sum(1 for _, _, _, status, _, _, _ in logs if status == "taken")
        missed_count = sum(1 for _, _, _, status, _, _, _ in logs if status == "missed")
        with_vitals = sum(1 for _, _, _, _, temp, hr, _ in logs if temp or hr)
        
        print(f"\n📊 Statistics:")
        print(f"   • Total Entries: {len(logs)}")
        print(f"   • Taken: {taken_count} | Missed: {missed_count}")
        print(f"   • With Vital Signs: {with_vitals}")
        print("=" * 85)
        input("\nPress Enter to continue...")
    except Exception as e:
        print(f"\n❌ Error viewing history: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to continue...")

def test_alarm():
    """Test alarm system with detailed feedback"""
    print("\n" + "=" * 70)
    print(" " * 20 + "🧪 ALARM SYSTEM TEST")
    print("=" * 70)
    print("\n📋 Testing Components:")
    print("   • Green LED (Heart Sensor) - Will blink")
    print("   • Red LED (Temperature Sensor) - Will blink")
    print("   • Blue LED (Button) - Will blink")
    print("   • Buzzer - Will sound")
    print("\n⏳ Starting test in 2 seconds...")
    time.sleep(2)
    
    print("\n🔔 TESTING NOW...")
    
    # Blink all LEDs and sound buzzer
    thread = threading.Thread(target=lambda: (
        blink_led(LED_HEART_PIN, 3, 0.2),
        blink_led(LED_TEMP_PIN, 3, 0.2),
        blink_led(LED_BUTTON_PIN, 3, 0.2),
        beep_buzzer(3, 0.1)
    ))
    thread.start()
    thread.join()
    
    print("\n✓ Alarm test complete!")
    print("   If you saw LEDs blink and heard buzzer, all components are working.")
    print("=" * 70)
    input("\nPress Enter to continue...")

def test_button():
    """Test button with real-time response - Press = Buzzer ON + Blue LED ON, Release = OFF"""
    print("\n" + "=" * 70)
    print(" " * 20 + "🔘 BUTTON TEST")
    print("=" * 70)
    print("\n📋 Test Instructions:")
    print("   • Press button → Blue LED turns ON + Buzzer sounds")
    print("   • Release button → Blue LED turns OFF + Buzzer stops")
    print("   • Press 'q' and Enter to exit test")
    print("\n⏳ Starting test in 2 seconds...")
    time.sleep(2)
    
    print("\n🔘 BUTTON TEST ACTIVE")
    print("   Press and hold the button to test...")
    print("   (Press 'q' + Enter to exit)\n")
    
    if GPIO is None:
        print("❌ GPIO not available. Cannot test button.")
        input("\nPress Enter to continue...")
        return
    
    # Test button state first
    print("🔍 Testing button connection...")
    initial_state = GPIO.input(BUTTON_PIN)
    print(f"   Initial button state: {'LOW (pressed?)' if initial_state == GPIO.LOW else 'HIGH (not pressed)'}")
    print("   (If button shows as pressed when not touching it, check wiring)\n")
    time.sleep(1)
    
    last_state = None
    last_print_time = 0
    press_count = 0
    release_count = 0
    
    print("   (Press Ctrl+C to exit)")
    try:
        while True:
            # Check if button is pressed (LOW = pressed, HIGH = not pressed)
            current_state = button_pressed()
            
            if current_state != last_state:
                current_time = time.time()
                # Always update hardware immediately
                if current_state:  # Button pressed
                    press_count += 1
                    if current_time - last_print_time > 0.2:  # Throttle prints
                        print(f"🔵 Button PRESSED (#{press_count}) → Blue LED ON + Buzzer ON")
                        last_print_time = current_time
                    led_on(LED_BUTTON_PIN)
                    buzzer_on()
                else:  # Button released
                    release_count += 1
                    if current_time - last_print_time > 0.2:  # Throttle prints
                        print(f"⚪ Button RELEASED (#{release_count}) → Blue LED OFF + Buzzer OFF")
                        last_print_time = current_time
                    led_off(LED_BUTTON_PIN)
                    buzzer_off()
                last_state = current_state
            
            time.sleep(0.02)  # Check every 20ms for better responsiveness
            
    except KeyboardInterrupt:
        pass
    finally:
        # Ensure everything is off
        led_off(LED_BUTTON_PIN)
        buzzer_off()
        print(f"\n✓ Button test complete!")
        print(f"   Total presses detected: {press_count}")
        print(f"   Total releases detected: {release_count}")
        print("=" * 70)
        input("\nPress Enter to continue...")

def get_active_medications():
    """Get all active medications sorted by schedule time"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT id, name, schedule_time FROM medications 
                 WHERE active = 1 ORDER BY schedule_time''')
    medications = c.fetchall()
    conn.close()
    return medications

def get_upcoming_medications():
    """Get upcoming medications for today"""
    current_time = datetime.datetime.now().strftime("%H:%M")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get all active medications scheduled after current time
    c.execute('''SELECT id, name, schedule_time FROM medications 
                 WHERE active = 1 AND schedule_time >= ? 
                 ORDER BY schedule_time LIMIT 5''', (current_time,))
    upcoming = c.fetchall()
    
    # Filter out already taken today
    filtered = []
    for med_id, name, schedule_time in upcoming:
        c.execute('''SELECT COUNT(*) FROM medication_logs 
                     WHERE medication_id = ? AND DATE(created_at) = ? AND status = 'taken' ''',
                  (med_id, current_date))
        already_taken = c.fetchone()[0] > 0
        if not already_taken:
            filtered.append((med_id, name, schedule_time))
    
    conn.close()
    return filtered

def display_monitoring_dashboard():
    """Display organized monitoring dashboard"""
    try:
        os.system('clear' if os.name != 'nt' else 'cls')
    except:
        pass  # If screen clear fails, just continue
    
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time_short = datetime.datetime.now().strftime("%H:%M")
    
    print("\n" + "=" * 70)
    print(" " * 15 + "💊 MEDHEALTH MONITORING DASHBOARD")
    print("=" * 70)
    
    # Current time and date
    print(f"\n📅 Date: {current_date}  |  🕐 Time: {current_time}")
    print("-" * 70)
    
    # Active medication schedule
    medications = get_active_medications()
    if medications:
        print("\n📋 ACTIVE MEDICATION SCHEDULE")
        print("─" * 70)
        print(f"{'Medication':<25} {'Schedule Time':<15} {'Status':<20}")
        print("─" * 70)
        
        for med_id, name, schedule_time in medications:
            # Check if taken today
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('''SELECT status, actual_time FROM medication_logs 
                         WHERE medication_id = ? AND DATE(created_at) = ? 
                         ORDER BY created_at DESC LIMIT 1''',
                      (med_id, current_date))
            result = c.fetchone()
            conn.close()
            
            if result:
                status, actual_time = result
                if status == "taken":
                    status_display = f"✓ Taken at {actual_time}"
                else:
                    status_display = "✗ Missed"
            else:
                # Check if time has passed
                if schedule_time <= current_time_short:
                    status_display = "⏰ Pending"
                else:
                    status_display = "⏳ Upcoming"
            
            print(f"{name:<25} {schedule_time:<15} {status_display:<20}")
        print("─" * 70)
    else:
        print("\n📋 No active medications scheduled")
    
    # Upcoming medications (next 3)
    upcoming = get_upcoming_medications()
    if upcoming:
        print("\n⏰ NEXT UPCOMING MEDICATIONS")
        print("─" * 70)
        for i, (med_id, name, schedule_time) in enumerate(upcoming[:3], 1):
            # Calculate time until
            now = datetime.datetime.now()
            scheduled = datetime.datetime.strptime(f"{current_date} {schedule_time}", "%Y-%m-%d %H:%M")
            time_diff = scheduled - now
            if time_diff.total_seconds() > 0:
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                if hours > 0:
                    time_until = f"{hours}h {minutes}m"
                else:
                    time_until = f"{minutes}m"
                print(f"  {i}. {name} at {schedule_time} (in {time_until})")
        print("─" * 70)
    
    print("\n" + "=" * 70)

def check_health_monitoring():
    """Check health parameters and trigger alarms if abnormal"""
    global alarm_active
    
    if not monitoring_active:
        return
    
    temp = read_temperature()
    hr = read_heart_rate()
    
    # Check temperature
    temp_alert = False
    if temp:
        if temp < TEMP_MIN or temp > TEMP_MAX:
            if not alarm_active:
                alarm_active = True
                temp_alert = True
                print(f"\n" + "!" * 70)
                print(f"⚠️  ALERT: Abnormal Temperature: {temp}°C (Normal: {TEMP_MIN}°C - {TEMP_MAX}°C)")
                print("!" * 70)
                # Blink temp LED and sound buzzer
                threading.Thread(target=lambda: (
                    blink_led(LED_TEMP_PIN, 5, 0.3),
                    beep_buzzer(5, 0.1)
                ), daemon=True).start()
            alarm_active = False
    
    # Check heart rate
    hr_alert = False
    if hr:
        if hr < HR_MIN or hr > HR_MAX:
            if not alarm_active:
                alarm_active = True
                hr_alert = True
                print(f"\n" + "!" * 70)
                print(f"⚠️  ALERT: Abnormal Heart Rate: {hr} bpm (Normal: {HR_MIN} - {HR_MAX} bpm)")
                print("!" * 70)
                # Blink heart LED and sound buzzer
                threading.Thread(target=lambda: (
                    blink_led(LED_HEART_PIN, 5, 0.3),
                    beep_buzzer(5, 0.1)
                ), daemon=True).start()
            alarm_active = False
    
    # Normal readings display
    if temp and hr:
        status = "✅ NORMAL"
        if temp_alert or hr_alert:
            status = "⚠️  ALERT"
        print(f"\r📊 Vital Signs: Temp={temp}°C | HR={hr} bpm | Status: {status}", end='', flush=True)

def medication_alarm_monitoring():
    """Independent medication alarm monitoring - runs continuously"""
    global alarm_active, alarm_monitoring_active
    
    while alarm_monitoring_active and system_running:
        try:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_time_full = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            
            # Get ALL active medications (not just exact match)
            c.execute('''SELECT id, name, schedule_time FROM medications 
                         WHERE active = 1''')
            all_medications = c.fetchall()
            
            # Check each medication to see if it's time
            for med_id, name, schedule_time in all_medications:
                # Parse scheduled time
                try:
                    scheduled_hour, scheduled_min = map(int, schedule_time.split(':'))
                    scheduled_datetime = now.replace(hour=scheduled_hour, minute=scheduled_min, second=0, microsecond=0)
                    
                    # Calculate time difference
                    time_diff = abs((now - scheduled_datetime).total_seconds())
                    
                    # Trigger alarm if within 30 seconds of scheduled time (before or after)
                    # This ensures we catch the alarm even if check happens slightly before/after
                    if time_diff <= 30:  # Within 30 seconds window
                        # Check if already logged today
                        c.execute('''SELECT COUNT(*) FROM medication_logs 
                                     WHERE medication_id = ? AND DATE(created_at) = ? AND status = 'taken' ''',
                                  (med_id, current_date))
                        already_logged = c.fetchone()[0] > 0
                        
                        if not already_logged:
                            # Display alert banner
                            print("\n" + "🔔" * 35)
                            print(f"⚠️  MEDICATION REMINDER")
                            print(f"💊 {name}")
                            print(f"⏰ Scheduled Time: {schedule_time}")
                            print(f"🕐 Current Time: {current_time_full}")
                            print(f"📅 {current_date}")
                            print("🔔" * 35)
                            print("\n👉 Press button to confirm medication intake...")
                            print("⏳ Waiting up to 60 seconds...")
                            print("🔊 ALARM ACTIVATED - Buzzer should be beeping now!")
                            
                            # Trigger alarm
                            alarm_active = True
                            
                            # Blink button LED and sound buzzer
                            alarm_thread = threading.Thread(target=medication_alarm, args=(60,), daemon=True)
                            alarm_thread.start()
                            print("✓ Alarm thread started - Buzzer and LED should be active")
                            
                            # Wait for button press (up to 60 seconds)
                            button_pressed_flag = wait_for_button(60)
                    
                            if button_pressed_flag:
                                # Stop alarm
                                alarm_active = False
                                buzzer_off()
                                led_off(LED_BUTTON_PIN)
                                
                                # Confirm medication taken
                                actual_time = datetime.datetime.now().strftime("%H:%M:%S")
                                
                                print("\n✓ Medication confirmed! Processing...")
                                
                                # Continuous beep and Blue LED on for 2 seconds (indicates medicine taken)
                                print("🔵 Blue LED ON + Continuous beep for 2 seconds...")
                                led_on(LED_BUTTON_PIN)  # Blue LED near button
                                continuous_beep(2.0)  # Continuous beep for 2 seconds
                                led_off(LED_BUTTON_PIN)
                                
                                # Ask about vitals
                                print("\n" + "─" * 70)
                                print("📊 OPTIONAL: Measure vital signs now?")
                                print("   Press button within 5 seconds to measure temperature & heart rate")
                                print("   Or wait 5 seconds to skip vitals measurement")
                                print("─" * 70)
                                measure_vitals = wait_for_button(5)
                                
                                temp = None
                                hr = None
                                if measure_vitals:
                                    print("\n📊 Measuring vital signs...")
                                    temp, hr = measure_vitals_manual()
                                else:
                                    print("\n⏭️  Skipping vital signs measurement")
                                
                                # Log medication
                                log_medication(med_id, name, schedule_time, actual_time, "taken", temp, hr)
                                
                                print("\n✓ Medication intake logged successfully!")
                                print("─" * 70)
                            else:
                                # Medication missed
                                alarm_active = False
                                buzzer_off()
                                led_off(LED_BUTTON_PIN)
                                actual_time = datetime.datetime.now().strftime("%H:%M:%S")
                                
                                print("\n" + "✗" * 35)
                                print(f"✗ Medication '{name}' was not confirmed")
                                print(f"   Scheduled: {schedule_time} | Status: MISSED")
                                print("✗" * 35)
                                
                                log_medication(med_id, name, schedule_time, actual_time, "missed")
                            
                            # Break out of loop after handling one medication alarm
                            # This prevents multiple alarms from triggering simultaneously
                            break
                except (ValueError, AttributeError) as e:
                    # Skip medications with invalid time format
                    continue
            
            conn.close()
            time.sleep(5)  # Check every 5 seconds for better accuracy
            
        except Exception as e:
            print(f"Error in medication alarm monitoring: {e}")
            time.sleep(5)

def medication_monitoring():
    """Monitor medication schedule - DEPRECATED: Now handled by medication_alarm_monitoring"""
    # This function is kept for compatibility but medication alarms now run independently
    pass
    
    while monitoring_active and system_running:
        try:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            current_time_full = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")
            
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            
            # Get ALL active medications (not just exact match)
            c.execute('''SELECT id, name, schedule_time FROM medications 
                         WHERE active = 1''')
            all_medications = c.fetchall()
            
            # Check each medication to see if it's time
            for med_id, name, schedule_time in all_medications:
                # Parse scheduled time
                try:
                    scheduled_hour, scheduled_min = map(int, schedule_time.split(':'))
                    scheduled_datetime = now.replace(hour=scheduled_hour, minute=scheduled_min, second=0, microsecond=0)
                    
                    # Calculate time difference
                    time_diff = abs((now - scheduled_datetime).total_seconds())
                    
                    # Trigger alarm if within 30 seconds of scheduled time (before or after)
                    # This ensures we catch the alarm even if check happens slightly before/after
                    if time_diff <= 30:  # Within 30 seconds window
                        # Check if already logged today
                        c.execute('''SELECT COUNT(*) FROM medication_logs 
                                     WHERE medication_id = ? AND DATE(created_at) = ? AND status = 'taken' ''',
                                  (med_id, current_date))
                        already_logged = c.fetchone()[0] > 0
                        
                        if not already_logged:
                            # Display alert banner
                            print("\n" + "🔔" * 35)
                            print(f"⚠️  MEDICATION REMINDER")
                            print(f"💊 {name}")
                            print(f"⏰ Scheduled Time: {schedule_time}")
                            print(f"🕐 Current Time: {current_time_full}")
                            print(f"📅 {current_date}")
                            print("🔔" * 35)
                            print("\n👉 Press button to confirm medication intake...")
                            print("⏳ Waiting up to 60 seconds...")
                            print("🔊 ALARM ACTIVATED - Buzzer should be beeping now!")
                            
                            # Trigger alarm
                            alarm_active = True
                            
                            # Blink button LED and sound buzzer
                            alarm_thread = threading.Thread(target=medication_alarm, args=(60,), daemon=True)
                            alarm_thread.start()
                            print("✓ Alarm thread started - Buzzer and LED should be active")
                            
                            # Wait for button press (up to 60 seconds)
                            button_pressed_flag = wait_for_button(60)
                    
                            if button_pressed_flag:
                                # Stop alarm
                                alarm_active = False
                                buzzer_off()
                                led_off(LED_BUTTON_PIN)
                                
                                # Confirm medication taken
                                actual_time = datetime.datetime.now().strftime("%H:%M:%S")
                                
                                print("\n✓ Medication confirmed! Processing...")
                                
                                # Continuous beep and Blue LED on for 2 seconds (indicates medicine taken)
                                print("🔵 Blue LED ON + Continuous beep for 2 seconds...")
                                led_on(LED_BUTTON_PIN)  # Blue LED near button
                                continuous_beep(2.0)  # Continuous beep for 2 seconds
                                led_off(LED_BUTTON_PIN)
                                
                                # Ask about vitals
                                print("\n" + "─" * 70)
                                print("📊 OPTIONAL: Measure vital signs now?")
                                print("   Press button within 5 seconds to measure temperature & heart rate")
                                print("   Or wait 5 seconds to skip vitals measurement")
                                print("─" * 70)
                                measure_vitals = wait_for_button(5)
                                
                                temp = None
                                hr = None
                                if measure_vitals:
                                    print("\n📊 Measuring vital signs...")
                                    temp, hr = measure_vitals_manual()
                                else:
                                    print("\n⏭️  Skipping vital signs measurement")
                                
                                # Log medication
                                log_medication(med_id, name, schedule_time, actual_time, "taken", temp, hr)
                                
                                print("\n✓ Medication intake logged successfully!")
                                print("─" * 70)
                                
                                # Update dashboard after a moment
                                time.sleep(2)
                                display_monitoring_dashboard()
                            else:
                                # Medication missed
                                alarm_active = False
                                buzzer_off()
                                led_off(LED_BUTTON_PIN)
                                actual_time = datetime.datetime.now().strftime("%H:%M:%S")
                                
                                print("\n" + "✗" * 35)
                                print(f"✗ Medication '{name}' was not confirmed")
                                print(f"   Scheduled: {schedule_time} | Status: MISSED")
                                print("✗" * 35)
                                
                                log_medication(med_id, name, schedule_time, actual_time, "missed")
                                
                                # Update dashboard after a moment
                                time.sleep(2)
                                display_monitoring_dashboard()
                            
                            # Break out of loop after handling one medication alarm
                            # This prevents multiple alarms from triggering simultaneously
                            break
                except (ValueError, AttributeError) as e:
                    # Skip medications with invalid time format
                    continue
            
            conn.close()
            time.sleep(5)  # Check every 5 seconds for better accuracy
            
        except Exception as e:
            print(f"Error in medication monitoring: {e}")
            time.sleep(30)

def medication_alarm(duration=60):
    """Medication alarm with LED blink and buzzer - loud and clear beeping pattern"""
    end_time = time.time() + duration
    while time.time() < end_time and alarm_active:
        # Fast, loud beeping pattern for maximum audibility
        for _ in range(4):  # 4 quick beeps per cycle
            led_on(LED_BUTTON_PIN)
            buzzer_on()
            time.sleep(0.15)  # On time for clear beep
            led_off(LED_BUTTON_PIN)
            buzzer_off()
            time.sleep(0.05)  # Very short pause between beeps
        # Short pause between beep groups
        time.sleep(0.2)

def health_monitoring():
    """Continuous health monitoring"""
    while monitoring_active and system_running:
        check_health_monitoring()
        time.sleep(10)  # Check every 10 seconds

def monitoring_status_updater():
    """Update monitoring dashboard every minute"""
    last_update = 0
    while monitoring_active and system_running:
        try:
            current_time_seconds = time.time()
            # Update dashboard every 30 seconds
            if current_time_seconds - last_update >= 30:
                display_monitoring_dashboard()
                last_update = current_time_seconds
            time.sleep(5)
        except Exception as e:
            print(f"Dashboard update error: {e}")
            time.sleep(5)

def start_alarm_monitoring():
    """Start independent medication alarm monitoring"""
    global alarm_monitoring_active, alarm_monitoring_thread
    
    if alarm_monitoring_active:
        return  # Already running
    
    alarm_monitoring_active = True
    alarm_monitoring_thread = threading.Thread(target=medication_alarm_monitoring, daemon=True)
    alarm_monitoring_thread.start()
    print("✓ Medication alarm monitoring started (runs independently)")

def stop_alarm_monitoring():
    """Stop independent medication alarm monitoring"""
    global alarm_monitoring_active
    alarm_monitoring_active = False
    alarm_active = False

def start_monitoring():
    """Start continuous health monitoring (vitals only) - Alarm works independently"""
    global monitoring_active
    
    if monitoring_active:
        print("\n⚠️  Monitoring is already active!")
        return
    
    # Display initial dashboard
    display_monitoring_dashboard()
    
    monitoring_active = True
    print("\n" + "─" * 70)
    print("🚀 HEALTH MONITORING ACTIVATED")
    print("─" * 70)
    print("  • Health monitoring: Every 10 seconds (temperature & heart rate)")
    print("  • Dashboard updates: Every 30 seconds")
    print("  • Medication alarms: Running independently (not affected by this)")
    print("  • Press Ctrl+C to stop monitoring")
    print("─" * 70)
    print("\n⏳ Starting health monitoring...\n")
    
    # Start only health monitoring threads (alarm monitoring runs independently)
    health_thread = threading.Thread(target=health_monitoring, daemon=True)
    dashboard_thread = threading.Thread(target=monitoring_status_updater, daemon=True)
    
    health_thread.start()
    dashboard_thread.start()
    
    # Give threads a moment to start
    time.sleep(2)
    
    try:
        while monitoring_active:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_monitoring()

def stop_monitoring():
    """Stop continuous health monitoring (alarm monitoring continues independently)"""
    global monitoring_active
    monitoring_active = False
    # Note: We don't stop alarm_active here because alarm monitoring is independent
    # Only turn off health monitoring LEDs/buzzer if they were on
    buzzer_off()
    led_off(LED_HEART_PIN)
    led_off(LED_TEMP_PIN)
    # Don't turn off LED_BUTTON_PIN as it might be used by alarm
    print("\n✓ Health monitoring stopped (medication alarms continue independently)")

def cleanup():
    """Cleanup GPIO and exit - ensure all LEDs are OFF"""
    global system_running, pwm_buzzer
    system_running = False
    stop_monitoring()
    
    # Stop PWM buzzer if it exists
    if pwm_buzzer:
        try:
            pwm_buzzer.stop()
            pwm_buzzer = None
        except:
            pass
    
    # Explicitly turn off all LEDs and buzzer before cleanup
    if GPIO:
        try:
            buzzer_off()  # Use function to properly turn off buzzer
            GPIO.output(LED_HEART_PIN, GPIO.LOW)
            GPIO.output(LED_TEMP_PIN, GPIO.LOW)
            GPIO.output(LED_BUTTON_PIN, GPIO.LOW)
            time.sleep(0.1)  # Small delay to ensure states are set
            GPIO.cleanup()
        except:
            # If cleanup fails, try to at least turn off LEDs
            try:
                buzzer_off()
                GPIO.output(LED_HEART_PIN, GPIO.LOW)
                GPIO.output(LED_TEMP_PIN, GPIO.LOW)
                GPIO.output(LED_BUTTON_PIN, GPIO.LOW)
            except:
                pass
    
    print("\n👋 System shutdown complete. All LEDs turned OFF. Goodbye!")

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    cleanup()
    sys.exit(0)

def main_menu():
    """Display main menu with improved formatting"""
    while system_running:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        print("\n" + "=" * 70)
        print(" " * 18 + "💊 MEDHEALTH SYSTEM")
        print("=" * 70)
        print(f"🕐 Current Time: {current_time}")
        print("─" * 70)
        print("1. ➕ Add Medication")
        print("2. 📋 View Medications")
        print("3. 🗑️  Delete Medication")
        print("4. 📊 Measure Vitals (Manual)")
        print("5. 📈 View Medication History")
        print("6. 🧪 Test Alarm")
        print("7. 🚀 Start Monitoring")
        print("8. 🚪 Exit")
        print("─" * 70)
        
        # Show quick status
        medications = get_active_medications()
        if medications:
            print(f"📋 Active Medications: {len(medications)}")
        else:
            print("📋 No active medications")
        
        print("=" * 70)
        
        choice = input("\n👉 Select an option (1-8): ").strip()
        
        if choice == "1":
            name = input("Enter medication name: ").strip()
            schedule_time = input("Enter schedule time (HH:MM format, e.g., 08:00): ").strip()
            try:
                datetime.datetime.strptime(schedule_time, "%H:%M")
                add_medication(name, schedule_time)
            except ValueError:
                print("⚠️  Invalid time format. Use HH:MM (e.g., 08:00)")
        
        elif choice == "2":
            view_medications()
        
        elif choice == "3":
            view_medications()
            try:
                med_id = int(input("\nEnter medication ID to delete: ").strip())
                delete_medication(med_id)
            except ValueError:
                print("⚠️  Invalid ID")
        
        elif choice == "4":
            measure_vitals_manual()
        
        elif choice == "5":
            view_history()
        
        elif choice == "6":
            print("\n" + "─" * 70)
            print(" " * 15 + "🧪 TEST MENU")
            print("─" * 70)
            print("1. Test Alarm (LEDs + Buzzer)")
            print("2. Test Button (Press/Release)")
            print("3. Back to Main Menu")
            print("─" * 70)
            test_choice = input("\n👉 Select test option (1-3): ").strip()
            
            if test_choice == "1":
                test_alarm()
            elif test_choice == "2":
                test_button()
            elif test_choice == "3":
                continue
            else:
                print("⚠️  Invalid option. Returning to main menu.")
        
        elif choice == "7":
            start_monitoring()
        
        elif choice == "8":
            cleanup()
            break
        
        else:
            print("⚠️  Invalid option. Please select 1-8.")

if __name__ == "__main__":
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    print("💊 MEDHEALTH SYSTEM - Initializing...")
    
    # Initialize components
    init_database()
    init_gpio()
    init_sensors()
    
    print("✓ System ready!\n")
    
    # Start independent medication alarm monitoring (runs always)
    start_alarm_monitoring()
    print("✓ Medication alarm monitoring is active (independent of Start Monitoring)\n")
    
    # Run main menu
    try:
        main_menu()
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        cleanup()

