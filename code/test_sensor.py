import RPi.GPIO as GPIO
import time

CS = 17
CLK = 18
DO = 23

def init_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CS, GPIO.OUT)
    GPIO.setup(CLK, GPIO.OUT)
    GPIO.setup(DO, GPIO.IN)

def read_sensor():
    GPIO.output(CS, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(CS, GPIO.LOW)
    time.sleep(0.001)
    
    data = 0
    for i in range(10):
        GPIO.output(CLK, GPIO.HIGH)
        time.sleep(0.001)
        data = data << 1
        if GPIO.input(DO) == GPIO.HIGH:
            data |= 1
        GPIO.output(CLK, GPIO.LOW)
        time.sleep(0.001)
    
    GPIO.output(CS, GPIO.HIGH)
    return data

if __name__ == '__main__':
    init_GPIO()
    try:
        while True:
            humidity_raw = read_sensor()
            print(f"Original humidity value：{humidity_raw}")
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
