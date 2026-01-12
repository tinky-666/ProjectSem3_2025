import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

# Pin configuration (match test_sensor.py)
CS_PIN = 17
CLK_PIN = 18
DO_PIN = 23

# Initialize GPIO for sensor
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.setup(CLK_PIN, GPIO.OUT)
    GPIO.setup(DO_PIN, GPIO.IN)

# Read raw humidity from sensor
def read_humidity():
    GPIO.output(CS_PIN, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CS_PIN, GPIO.LOW)
    time.sleep(0.001)
    
    raw_data = 0
    for i in range(10):
        GPIO.output(CLK_PIN, GPIO.HIGH)
        time.sleep(0.001)
        raw_data = raw_data << 1
        if GPIO.input(DO_PIN) == GPIO.HIGH:
            raw_data |= 1
        GPIO.output(CLK_PIN, GPIO.LOW)
        time.sleep(0.001)
    
    GPIO.output(CS_PIN, GPIO.HIGH)
    return raw_data

# Read temperature (placeholder: replace with DHT11/DHT22 code if available)
def read_temperature():
    # Return fixed value if no temperature sensor; update if sensor is connected
    return 25.0  # Unit: °C

def main():
    init_gpio()
    # Define path for data storage (Raspberry Pi path)
    data_path = "/home/pi/ProjectSem3_2025/data/sensor_data.csv"
    
    # Create CSV file and write header
    with open(data_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['timestamp', 'humidity_raw', 'temperature_celsius'])
    
    print("Data collection started. Will run for 48 hours (30-minute intervals).")
    print("Press Ctrl+C to stop early (not recommended).")
    
    try:
        start_time = time.time()
        while time.time() - start_time < 28800:
            # Get current timestamp (format: YYYY-MM-DD HH:MM:SS)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Read sensor data
            humidity_raw = read_humidity()
            temperature = read_temperature()
            # Write data to CSV
            with open(data_path, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([current_time, humidity_raw, temperature])
            # Print status
            print(f"Collected: {current_time} | Humidity: {humidity_raw} | Temp: {temperature}°C")
            # Wait for 30 minutes (1800 seconds) before next collection
            time.sleep(1800)
    except KeyboardInterrupt:
        print("\nData collection interrupted. Cleaning up GPIO...")
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
        print("Data collection stopped. Data saved to:", data_path)

if __name__ == '__main__':
    main()
