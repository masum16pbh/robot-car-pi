import pygame
import asyncio
import websockets
import json

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Car Driving Using WebSocket')
clock = pygame.time.Clock()

# Game state
car = {
    'x': 300,
    'y': 200,
    'size': 40,
    'color': (0, 255, 0),
    'velocity_x': 0,
    'velocity_y': 0,
    'speed': 3
}

# Movement functions
def move_up():
    car['velocity_x'], car['velocity_y'] = 0, -car['speed']

def move_down():
    car['velocity_x'], car['velocity_y'] = 0, car['speed']

def move_left():
    car['velocity_x'], car['velocity_y'] = -car['speed'], 0

def move_right():
    car['velocity_x'], car['velocity_y'] = car['speed'], 0

def stop():
    car['velocity_x'], car['velocity_y'] = 0, 0

# WebSocket handler
async def handle_client(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)
            command = data.get('command')
            
            if command == "up": move_up()
            elif command == "down": move_down()
            elif command == "left": move_left()
            elif command == "right": move_right()
            else: stop()
            
            # Send back current position
            await websocket.send(json.dumps({
                'x': car['x'],
                'y': car['y'],
                'status': 'OK'
            }))
        except Exception as e:
            await websocket.send(json.dumps({'error': str(e)}))

# Pygame loop
async def game_loop():
    running = True
    while running:
        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update position
        car['x'] += car['velocity_x']
        car['y'] += car['velocity_y']
        
        # Keep car on screen
        car['x'] = max(0, min(car['x'], 800 - car['size']))
        car['y'] = max(0, min(car['y'], 600 - car['size']))
        
        # Draw everything
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, car['color'], 
                        (car['x'], car['y'], car['size'], car['size']))
        pygame.display.flip()
        
        # Yield to event loop
        await asyncio.sleep(0.016)  # ~60fps
        clock.tick(60)

async def main():
    # Start WebSocket server
    ws_server = await websockets.serve(
        handle_client, "localhost", 8000
    )
    
    print("WebSocket server started at ws://localhost:8000")
    print("Open client.html in a browser to control the car")
    
    # Run game loop
    await game_loop()
    
    # Cleanup
    ws_server.close()
    await ws_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())