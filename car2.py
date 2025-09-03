# main_program.py
import asyncio
import websockets
from websockets.asyncio.server import serve
import json

async def handle_command(websocket,path):
    async for command in websocket:
        data = json.loads(command)
        message = data.get('command')
        if message == "forward":
            move_forward()
        elif message == "left":
            turn_left()
        elif message == "right":
            turn_right()
        elif message =="back":
            move_backword()
        else:
            print("Unknown command")

def move_forward():
    print("Moving forward...")

def turn_left():
    print("Turning left...")

def turn_right():
    print("Turning Right...")

def move_backword():
    print("Moving Backword...")


async def main():
    server = await websockets.serve(handle_command, 'localhost', 8000)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

