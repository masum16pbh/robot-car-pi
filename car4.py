from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pygame
from pygame.locals import *
import threading

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Car Driving using web browser")
clock = pygame.time.Clock()

car_color = (0,255,0)
car_size = 40
car_x,car_y = 300, 200
velocity_x, velocity_y = 0,0
speed = 1

def move_up():
    global velocity_x,velocity_y
    velocity_x, velocity_y = 0,-speed

def move_down():
    global velocity_x, velocity_y
    velocity_x, velocity_y = 0, speed

def move_left():
    global velocity_x, velocity_y
    velocity_x, velocity_y = -speed, 0

def move_right():
    global velocity_x, velocity_y
    velocity_x, velocity_y = speed, 0

def stop():
    global velocity_x, velocity_y
    velocity_x, velocity_y = 0,0



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

def pygame_loop():
    global car_x, car_y, velocity_x,velocity_y
    running = True
    while running:
        for event in pygame.event.get():
            if event.type== QUIT:
                running = False
        
        #update car positon
        car_x += velocity_x
        car_y += velocity_y

        #drawing 
        screen.fill((8,54,82))
        pygame.draw.rect(screen,car_color,(car_x,car_y,car_size,car_size))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    flask_thread = threading.Thread(
        target=lambda: socketio.run(app, port=7890, debug=False, use_reloader=False),
        daemon=True
    )       
    flask_thread.start()
    pygame_loop()