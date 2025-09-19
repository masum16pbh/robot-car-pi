import math
with open("pathset.txt", "r") as f:
    data = f.read()
points = []
for line in data.split('),'):
    x, y = map(int, line.strip('() \n').split(','))
    points.append((x, y))

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

    if turn_angle == 0:
        turn_direction = "Straight"
    if turn_angle > 0:
        turn_direction = "Left"
        
    elif turn_angle < 0:
        turn_direction = "Right"
            
        
    print(f"Line from ({x1}, {y1}) to ({x2}, {y2})Distance: {distance:.2f} units, Angle: {angle:.2f} degrees")
    print(f"Turn {turn_direction} by {abs(turn_angle):.2f} degrees")
