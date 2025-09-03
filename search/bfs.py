import queue
import networkx as nx
import matplotlib.pyplot as plt
import time

# BFS Implementation
def order_bfs(graph, start_node):
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []
    while not q.empty():
        vertex = q.get()
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for neighbor in graph.neighbors(vertex):  # Use NetworkX neighbors
                if neighbor not in visited:
                    q.put(neighbor)
    return order


# Visualization Function
def visualize_search(order, title, G, pos):
    plt.figure()
    plt.title(title)
    for i, node in enumerate(order, start=1):
        plt.clf()
        plt.title(title)
        # Highlight the currently visited node in red, others in green
        nx.draw(
            G, pos, with_labels=True,
            node_color=['r' if n == node else 'g' for n in G.nodes]
        )
        plt.draw()
        plt.pause(0.5)  # Pause to visualize each step
    plt.show()
    time.sleep(0.5)

def generate_connected_random_graph(n,m):
    while True:
        G = nx.gnm_random_graph(n,m)
        if nx.is_connected(G):
            return G
G = generate_connected_random_graph(20,19)
'''# Define Graph
G = nx.Graph()
G.add_edges_from([
    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('E', 'B'),
    ('B', 'F'), ('C', 'G'), ('D', 'H'), ('D', 'I')
])'''
pos = nx.spring_layout(G)  # Define layout for visualization

# Visualize BFS
bfs_order = order_bfs(G, 1)
print(bfs_order)
visualize_search(bfs_order, 'BFS Visualization', G, pos)

