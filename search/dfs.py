
import networkx as nx
import matplotlib.pyplot as plt
import time


def order_dfs(graph, start_node, visited=None):
    if visited is None:
        visited = set()

    order = []
    if start_node not in visited:
        order.append(start_node)
        visited.add(start_node)
        for neighbor in graph.neighbors(start_node):  # Use NetworkX neighbors
            if neighbor not in visited:
                order.extend(order_dfs(graph, neighbor, visited))
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
#G = generate_connected_random_graph(20,19)
# Define Graph
G = nx.Graph()
edge_list = [
    ('A', 'B'), ('A', 'C'), ('A', 'D'), ('E', 'B'),
    ('B', 'F'), ('C', 'G'), ('D', 'H'), ('D', 'I')
]
G.add_edges_from(edge_list)
pos = nx.planar_layout(G)


dfs_order = order_dfs(G, 'A')
print(dfs_order)
visualize_search(dfs_order, 'DFS Visualization', G, pos)
