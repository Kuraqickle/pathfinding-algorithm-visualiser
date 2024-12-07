# pathfinding-algorithm-visualiser

This project is an interactive tool that shows how pathfinding algorithms like Dijkstra’s, A*, and Depth-First Search work. You can create a grid, set a starting point and an endpoint, add walls as obstacles, and watch the algorithm find the shortest path in real-time. It’s a fun way to explore and understand how these algorithms navigate through spaces.

To use it, simply click on the grid to place the start and end points, draw walls, and choose an algorithm. Then hit the run key to see it in action. You can reset the grid at any time to experiment with different layouts or algorithms.

To get started, clone the repository, install Pygame with pip install pygame, and run the script with Python.

Below are the controls for interacting with the Pathfinding Algorithm Visualizer. Use these keys to select algorithms, run visualizations, and reset the grid:

D Key: Selects Dijkstra's Algorithm. This is a guaranteed shortest-path algorithm that explores all possible paths in an optimal way.

A Key: Selects the A* algorithm. This is a heuristic-based algorithm that often finds the path faster by considering the distance to the endpoint during exploration.

S Key: Selects Depth-First Search (DFS). This is a less efficient algorithm for pathfinding, as it explores deeply into one path before backtracking, and it does not guarantee the shortest path.

F Key: Runs the selected algorithm. After setting the start and end points and any walls, pressing F begins the visualization of the currently selected pathfinding algorithm.

G Key: Resets the grid. Clears all walls, the start and end points, and any algorithm progress, allowing you to start over with a new setup.
