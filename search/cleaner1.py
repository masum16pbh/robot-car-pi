import matplotlib.pyplot as plt
def dfs_clean(room, x, y, rows, cols, visited):
    if x < 0 or x >= rows or y < 0 or y >= cols or room[x][y] == 'o' or (x, y) in visited:
        return

    visited.add((x, y))
    if room[x][y] == 'd':
        print(f"Cleaning cell: ({x}, {y})")
        room[x][y] = 'c'

    # Visit all 4 neighboring cells
    dfs_clean(room, x + 1, y, rows, cols, visited)  # Down
    dfs_clean(room, x - 1, y, rows, cols, visited)  # Up
    dfs_clean(room, x, y + 1, rows, cols, visited)  # Right
    dfs_clean(room, x, y - 1, rows, cols, visited)  # Left


def clean_room(room, start_x, start_y):
    rows = len(room)
    cols = len(room[0]) if rows > 0 else 0
    visited = set()

    dfs_clean(room, start_x, start_y, rows, cols, visited)

    # Print the final state of the room
    print("Final room state:")
    for row in room:
        print(" ".join(row))

def visualize_room(room, title = "Room Cleaning",delay = .5):
    color_map = {'d': 'gray', 'c': 'white', 'o': 'red', 'current': 'green'}
    rows = len(room)
    cols = len(room[0])
    grid_colors = [[color_map[room[r][c]] for c in range(cols)] for r in range(rows)]

    plt.figure(figsize=(6, 6))
    plt.title(title)
    plt.imshow(grid_colors, interpolation='nearest', extent=(0, cols, rows, 0))
    plt.xticks(range(cols))
    plt.yticks(range(rows))
    plt.grid(visible=True, which='both', color='black', linestyle='-', linewidth=1)
    plt.show(block=False)
    plt.pause(delay)
    plt.close()
# Example room
f = open("room.text","r")
room = [[s for s in line.split()]for line in f]
# Start cleaning from position (0, 0)
start_x, start_y = 0, 0
clean_room(room, start_x, start_y)
