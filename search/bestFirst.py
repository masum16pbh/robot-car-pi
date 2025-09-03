import networkx as nx
import matplotlib.pyplot as plt
import heapq

def best_first_search(graph, start, goal, heuristic):
    # Priority queue to store (heuristic value, current node, path)
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic[start], start, [start]))
    visited = set()

    while priority_queue:
        # Get the node with the smallest heuristic value
        _, current_node, path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        # If the goal is reached, return the path
        if current_node == goal:
            return path

        # Explore neighbors
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (heuristic[neighbor], neighbor, path + [neighbor]))
    plt.show()
    return None  # Return None if no path is found

# Define the graph and heuristic
G = nx.Graph()
edges = [
    ("A", "B", 1),
    ("A", "C", 3),
    ("B", "D", 4),
    ("B", "E", 2),
    ("C", "F", 5),
    ("D", "G", 2),
    ("E", "G", 3),
    ("F", "G", 1),
]

# Add edges to the graph
for u, v, weight in edges:
    G.add_edge(u, v, weight=weight)

# Define heuristic values
heuristic = {
    "A": 6,
    "B": 4,
    "C": 5,
    "D": 2,
    "E": 3,
    "F": 4,
    "G": 0
}

# Perform Best-First Search
start_node = "A"
goal_node = "G"
path = best_first_search(G, start_node, goal_node, heuristic)

# Visualize the graph and the path
pos = nx.spring_layout(G)  # Layout for nodes
plt.figure(figsize=(10, 6))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

# Highlight the path
if path:
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found")

# Display the graph
plt.title("Best-First Search Visualization")
plt.show()
