import math
import RPi.GPIO as GPIO
import time
import threading
global stop_event
global start_time
global velocity 
velocity = 1 # units per second

motorL = 33  # GPIO pin for motor A
motorR = 32  # GPIO pin for motor B
LMF = 11
LMB = 13
RMA = 15
RMB = 16
TRIG = 23   # GPIO23 (pin 16)
ECHO = 24   # GPIO24 (pin 18)

GPIO.setmode(GPIO.BOARD)  # Stay consistent with BOARD mode
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorL, GPIO.OUT)
GPIO.setup(motorR, GPIO.OUT)
GPIO.setup(LMF, GPIO.OUT)
GPIO.setup(LMB, GPIO.OUT)   
GPIO.setup(RMA, GPIO.OUT)
GPIO.setup(RMB, GPIO.OUT)

pwmA = GPIO.PWM(motorL, 100)  # Set frequency to 100Hz
pwmB = GPIO.PWM(motorR, 100) # Set frequency to 100Hz

pwmA.start(28)  # Start PWM with 40% duty cycle
pwmB.start(25)  # Start PWM with 40% duty cycle

GPIO.output(LMF, GPIO.LOW)
GPIO.output(RMA, GPIO.LOW)
GPIO.output(LMB, GPIO.LOW)
GPIO.output(RMB, GPIO.LOW)
stop_event = threading.Event()

def move_up(distance):
    global start_time,remaining_distance,velocity
    remaining_distance = distance
    start_time = time.time()
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.HIGH)
    time.sleep(distance / velocity)  # Adjust the multiplier based on your calibration



def move_down():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(RMA, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    print("Moving down")

def move_left(turn_angle=90):
    print("Moving left")
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA,GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.HIGH)
    time.sleep(0.006*turn_angle)  
    return

    
def move_right(turn_angle=90):
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    print("Moving right")
    time.sleep(0.006*turn_angle)
    return

    
def stop():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    print("Stopped")



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
    distance = (elapsed * 34300) / 2  # in cm
    return distance

def obstacle_monitor():
    global remaining_distance, start_time,velocity
    while True:
        dist = get_distance()
        print(f"[Sensor] Distance: {dist:.2f} cm")

        if dist < 40 and not stop_event.is_set():  
            print("⚠️ Obstacle detected! Forcing STOP.")
            stop()
            stop_time = time.time()
            elasped = (stop_time - start_time)*velocity
            stop_event.set()
            
        elif stop_event == set and dist >= 75:
            stop_event.clear()
            if remaining_distance > 0:
                print("✅ Path clear. Resuming movement.")
                move_up(remaining_distance)
                
        time.sleep(0.06)

with open("pathset.txt", "r") as f:
    data = f.read()
points = []
for line in data.split('),'):
    x, y = map(int, line.strip('() \n').split(','))
    points.append((x, y))

#thread for obstacle detection
sensor_thread = threading.Thread(target=obstacle_monitor, daemon=True)
sensor_thread.start()


last_angel = 0 
for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        angle = 90 if dy > 0 else -90
    else:
        angle = math.degrees(math.atan2(dy, dx))

    distance = (dx** 2 + dy ** 2) ** 0.5

    #turn angle calculation
    turn_angle = angle - last_angel
    last_angel = angle
    # Normalize turn angle to the range [-180, 180] for easier control in cricical sinarios
    if turn_angle > 180:
        turn_angle = turn_angle - 360
    elif turn_angle < -180:
        turn_angle = 360 + turn_angle

    if turn_angle > 0:
        turn_direction = "Left"
        move_left(turn_angle)
    elif turn_angle < 0:
        turn_direction = "Right"
        move_right(turn_angle)
    if distance > 0:
        move_up(distance)
        
    print(f"Line from ({x1}, {y1}) to ({x2}, {y2})Distance: {distance:.2f} units, Angle: {angle:.2f} degrees")
    print(f"Turn {turn_direction} by {abs(turn_angle):.2f} degrees")


stop()
GPIO.cleanup()


