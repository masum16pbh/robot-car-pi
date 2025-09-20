import math
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BOARD)

global start_time, velocity, distance, stop_event, shutdown_event
velocity = 0.6  # units per second

motorL = 33
motorR = 32
LMF = 11
LMB = 13
RMA = 15
RMB = 16
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(motorL, GPIO.OUT)
GPIO.setup(motorR, GPIO.OUT)
GPIO.setup(LMF, GPIO.OUT)
GPIO.setup(LMB, GPIO.OUT)
GPIO.setup(RMA, GPIO.OUT)
GPIO.setup(RMB, GPIO.OUT)

pwmA = GPIO.PWM(motorL, 100)
pwmB = GPIO.PWM(motorR, 100)
pwmA.start(40)
pwmB.start(38)

stop_event = threading.Event()
shutdown_event = threading.Event()

def move_up(distance):
    """Move forward but allow interruption by obstacle monitor"""
    global start_time
    start_time = time.time()
    traveled = 0
    step_time = 0.1  # move in small time slices

    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.HIGH)

    while traveled < distance:
        if stop_event.is_set():
            stop()
            # Wait until obstacle cleared
            while stop_event.is_set():
                time.sleep(0.1)
            # Resume
            print("Path clear\nmove up")
            GPIO.output(LMF, GPIO.LOW)
            GPIO.output(RMA, GPIO.LOW)
            GPIO.output(LMB, GPIO.HIGH)
            GPIO.output(RMB, GPIO.HIGH)

        time.sleep(step_time)
        traveled += velocity * step_time
        print(f"Traveled: {traveled:.2f} cm, Target: {distance:.2f} cm")

    stop()

def move_down():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(RMA, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    print("Moving down")

def move_left(turn_angle=90):
    print("Moving left")
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.HIGH)
    time.sleep(0.006*abs(turn_angle))
    stop()

def move_right(turn_angle=90):
    print("Moving right")
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    time.sleep(0.006*abs(turn_angle))
    stop()

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
    distance = (elapsed * 34300) / 2
    return distance

def obstacle_monitor():
    global distance
    while not shutdown_event.is_set():
        dist = get_distance()
        print(f"[Sensor] Distance: {dist:.2f} cm")

        if 0 <= dist < 40 and not stop_event.is_set():
            print("⚠️ Obstacle detected! Forcing STOP.")
            stop()
            stop_event.set()

        elif stop_event.is_set() and dist >= 40:
            print("✅ Path clear. Resuming movement.")
            stop_event.clear()

        time.sleep(0.1)

# ---- PATH LOGIC ----
with open("line.txt", "r") as f:
    data = f.read()
points = []
for line in data.split('),'):
    x, y = map(int, line.strip('() \n').split(','))
    points.append((x, y))

# start sensor thread
sensor_thread = threading.Thread(target=obstacle_monitor, daemon=True)
sensor_thread.start()

last_angle = 0
for i in range(len(points) - 1):
    x1, y1 = points[i]
    x2, y2 = points[i + 1]
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0:
        angle = 90 if dy > 0 else -90
    else:
        angle = math.degrees(math.atan2(dy, dx))

    distance = (dx**2 + dy**2) ** 0.5
    turn_angle = angle - last_angle
    last_angle = angle

    if turn_angle > 180:
        turn_angle -= 360
    elif turn_angle < -180:
        turn_angle += 360

    if turn_angle == 0:
        print("straight line")
    elif turn_angle > 0:
        move_left(turn_angle)
    elif turn_angle < 0:
        move_right(turn_angle)

    if distance > 0:
        #while stop_event.is_set():
        #    time.sleep(0.1)  # wait until obstacle clears
        move_up(distance)

    print(f"Line from ({x1},{y1}) to ({x2},{y2}), Distance: {distance:.2f}, Angle: {angle:.2f}")

# ---- CLEAN EXIT ----
stop()
shutdown_event.set()   # stop the sensor thread
sensor_thread.join()   # wait for thread to finish
GPIO.cleanup()
