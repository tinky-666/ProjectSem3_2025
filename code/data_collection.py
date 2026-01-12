import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

# Sensor configuration
DO_PIN = 17  # BCM 17 (Physical Pin 11)
COLLECTION_DURATION = 28800  # 8 hours in seconds (adjust to 21600 for 6 hours)
SAMPLING_INTERVAL = 1800  # 30 minutes in seconds (adjust to 600 for 10 mins)

# Initialize GPIO
def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DO_PIN, GPIO.IN)

# Read soil moisture status (digital output)
def read_moisture_status():
    """Return 0 (WET) or 1 (DRY) + human-readable status"""
    digital_value = GPIO.input(DO_PIN)
    status = "WET" if digital_value == 0 else "DRY"
    return digital_value, status

# Main data collection function
def main():
    init_gpio()
    # Define file path (Raspberry Pi directory)
    data_file_path = "/home/pi/ProjectSem3_2025/data/sensor_data.csv"
    
    # Create CSV file and write header
    with open(data_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['timestamp', 'digital_value', 'soil_status'])
    
    print(f"Data collection started. Duration: {COLLECTION_DURATION/3600} hours | Interval: {SAMPLING_INTERVAL/60} minutes")
    print("Press Ctrl+C to stop early (not recommended).")
    
    try:
        start_time = time.time()
        # Collect data for specified duration
        while time.time() - start_time < COLLECTION_DURATION:
            # Get current timestamp (UTC+8)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Read sensor data
            digital_val, soil_stat = read_moisture_status()
            # Write to CSV
            with open(data_file_path, 'a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([current_time, digital_val, soil_stat])
            # Print status to terminal
            print(f"Collected: {current_time} | Value: {digital_val} | Status: {soil_stat}")
            # Wait for next sampling interval
            time.sleep(SAMPLING_INTERVAL)
    except KeyboardInterrupt:
        print("\nData collection interrupted by user.")
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
        print(f"Data collection finished. File saved to: {data_file_path}")

if __name__ == '__main__':
    main()
