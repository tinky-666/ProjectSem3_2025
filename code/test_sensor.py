import RPi.GPIO as GPIO
import time

# Configuration: Sensor DO pin connected to Raspberry Pi BCM 17 (Physical Pin 11)
DO_PIN = 17

# Initialize GPIO settings for sensor
def init_gpio():
    """Set up GPIO mode and configure DO pin as input"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DO_PIN, GPIO.IN)  # DO pin is input for digital signal

# Read soil moisture status from sensor
def read_soil_moisture():
    """
    Read digital output from sensor:
    - Return 0: Soil is WET (low level signal)
    - Return 1: Soil is DRY (high level signal)
    """
    return GPIO.input(DO_PIN)

# Main function: Continuous sensor testing
if __name__ == '__main__':
    init_gpio()
    try:
        print("Soil moisture sensor test started. Press Ctrl+C to stop.")
        while True:
            moisture_level = read_soil_moisture()
            # Translate digital value to human-readable status
            soil_status = "WET" if moisture_level == 0 else "DRY"
            print(f"Soil Status: {soil_status} | Digital Value: {moisture_level}")
            time.sleep(2)  # Read data every 2 seconds
    except KeyboardInterrupt:
        print("\nTest interrupted by user. Cleaning up GPIO resources...")
        GPIO.cleanup()  # Release GPIO pins
    finally:
        GPIO.cleanup()  # Ensure GPIO cleanup even if error occurs
        print("Sensor test completed successfully.")
