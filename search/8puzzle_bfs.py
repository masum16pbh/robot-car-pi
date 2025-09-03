from collections import deque
gole_state =[[1,2,3],[8,0,4],[7,6,5]]

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i,j


def get_neighbors(state):
    neighbors = []
    x,y = find_blank(state)
    direction = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx,dy in direction:
        nx,ny = x+dx, y+dy
        if 0<= nx< 3 and 0<= ny<3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def bfs(start):
    queue = deque([(start,[])])
    visited = set()

    while queue:
        current_state,path = queue.popleft()
        state_tuple = tuple(map(tuple, current_state))
        if current_state == gole_state:
            return path + current_state

        if state_tuple in visited:
            continue

        visited.add(state_tuple)
        for neighbor in get_neighbors(current_state):
            queue.appendleft((neighbor,path+[current_state]))
    return None

initial_state = [[1,2,3],[4,0,5],[8,7,6]]

solution = bfs(initial_state)
if solution:
    print("steps to solve puzzle using (BFS):")
    for state in solution:
        for row in state:
            print(row)
        print()
else:
    print("No solution found.")
