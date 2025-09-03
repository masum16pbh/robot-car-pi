import pygame
from pygame.locals import *
import asyncio
import websockets
from websockets.server import serve
import json

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Car Driving Using keyboard')
clock = pygame.time.Clock()

car_color = (0, 255, 0)
car_size = 40
car_x, car_y = 300, 200
velocity_x, velocity_y = 0, 0
speed = 1

def move_up():
    global velocity_x, velocity_y
    velocity_x, velocity_y = 0, -speed

def move_down():
    global velocity_x, velocity_y
    velocity_x, velocity_y = 0, speed

def move_left():
    global velocity_x, velocity_y
    velocity_x, velocity_y = -speed, 0

def move_right():
    global velocity_x, velocity_y
    velocity_x, velocity_y = speed, 0

def poss_game():
    global velocity_x, velocity_y
    velocity_x, velocity_y = 0, 0

async def handle_command(websocket,path):
    async for command in websocket:
        data = json.loads(command)
        message = data.get('command')
        print(message)
        if message == "forward":
            move_up()
        elif message == "left":
            move_left()
        elif message == "right":
            move_right()
        elif message == "back":
            move_down()
        else:
            poss_game()

async def pygame_loop():
    global car_x, car_y, running
    
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        
        # Update game state
        car_x, car_y = car_x + velocity_x, car_y + velocity_y
        
        # Draw everything
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, car_color, (car_x, car_y, car_size, car_size))
        pygame.display.flip()
        
        # Yield control to the event loop
        await asyncio.sleep(0)
        clock.tick(60)

async def main():
    # Start WebSocket server
    async with serve(handle_command, '0.0.0.0', 8000):
        await pygame_loop()
    


if __name__ == "__main__":
    asyncio.run(main())