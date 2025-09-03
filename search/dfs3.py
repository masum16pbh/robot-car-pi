import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

f = open('dirty.text','r')
room = [[int(s) for s in line.split() ]for line in f]
start_node =(0,4)
def order_dfs(graph,start_node):
    visited = set()
    stack = [start_node]
    order =[]
    row = len(room)
    col = len(room[0])
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            x,y = node
            neighbors=[
                (x-1,y),
                (x+1,y),
                (x,y-1),
                (x,y+1)
            ]
            valid_neighbors =[
                (nx,ny) for nx,ny in neighbors if 0<= nx<row and 0<= ny<col
                                                  and graph[nx][ny] >=0 and (nx,ny) not in visited

            ]
            stack.extend(valid_neighbors)

    return order
floor = room
order =order_dfs(room,(0,0))

print(order)
plt.imshow(floor,cmap='gray')
plt.show()