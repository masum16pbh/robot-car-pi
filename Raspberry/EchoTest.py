import RPi.GPIO as GPIO
import time
TRIG = 23   # GPIO23 (pin 16)
ECHO = 24   # GPIO24 (pin 18)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time, stop_time = 0, 0

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed = stop_time - start_time
    distance = (elapsed * 343) / 2  # in meter
    return distance

while True:
    dist = get_distance()
    print(dist)
    time.sleep(.3)