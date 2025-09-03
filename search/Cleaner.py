import matplotlib.pyplot as plt
import numpy as np

# Function to visualize the grid
def visualize_grid(grid, title="Grid Visualization"):
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.title(title)
    plt.draw()  # Draw the updated plot
    plt.pause(0.8)  # Pause to allow the update to render

# Example grid and cleaning simulation
grid = np.array([
    [3, 0, 2],
    [0, 0, 1],
    [2, 1, 0]
])

plt.figure()

# Simulating a cleaning process
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        if grid[i, j] > 0:
            print(f"Cleaning position ({i}, {j})")
            grid[i, j] = 0  # Simulate cleaning
            visualize_grid(grid, title=f"Cleaning Position ({i}, {j})")

plt.show()  # Display the final state
