from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time
import threading

motorL = 33  # GPIO pin for motor A
motorR = 32  # GPIO pin for motor B
LMF = 11
LMB = 13
RMA = 15
RMB = 16

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

def move_up():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.HIGH)


def move_down():
    GPIO.output(LMF, GPIO.HIGH)
    GPIO.output(RMA, GPIO.HIGH)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    print("Moving down")

def move_left():
    print("Moving left")
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA,GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.HIGH)

    
def move_right():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.HIGH)
    GPIO.output(RMB, GPIO.LOW)
    print("Moving right")

    
def stop():
    GPIO.output(LMF, GPIO.LOW)
    GPIO.output(RMA, GPIO.LOW)
    GPIO.output(LMB, GPIO.LOW)
    GPIO.output(RMB, GPIO.LOW)
    print("Stopped")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, async_mode='threading')


@app.route('/')
def index():
    return render_template('car4.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # Optionally notify frontend if you add a listener
    emit('car_response', '✅ Connected to server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    # Optionally notify frontend if you add a listener
    emit('car_response', '❌ Disconnected from server')


@socketio.on('car_command')   # 🔹 match frontend
def handle_car_command(command):
    print(f'Received command: {command}')
    if command == "up":
        move_up()
    elif command == "down":
        move_down()
    elif command == "left":
        move_left()
    elif command == "right":
        move_right()
    elif command == "stop":
        stop()
    # Send confirmation back to client(s)
    emit('car_response', f'Car moving {command}', broadcast=True)


if __name__ == '__main__':
    flask_thread = threading.Thread(
        target=lambda: socketio.run(app,host="192.168.0.121", port=7890, debug=False, use_reloader=False),
        daemon=True
    )       
    flask_thread.start()