import pygame
import sys
import heapq
import math

# Initialize Pygame
pygame.init()

# Set up the grid
width, height = 800, 600
cell_size = 25
rows, cols = height // cell_size, (width // cell_size) - 5  # Reduced columns for more space

# Define the area for displaying text
text_area_width = 300
text_area_height = 100
text_area_x = width


# Initialize the display
screen = pygame.display.set_mode((width + text_area_width, height + text_area_height))
pygame.display.set_caption("Pathfinding Visualization")

# Initialize font
pygame.font.init()
font = pygame.font.Font(None, 36)

# Variables for text display
algorithm_text = font.render("Algorithm: Dijkstra", True, pygame.Color("black"))
nodes_visited_text = font.render("Nodes visited: 0", True, pygame.Color("black"))

# Initialize the grid with zeros, where 0 represents an empty cell
grid = [[0] * cols for _ in range(rows)]

# Variables to store the positions of start and end points
start_point = None
end_point = None

# Variables for Dijkstra's algorithm
dijkstra_visited = set()
dijkstra_distances = {(i, j): float('inf') for j in range(cols) for i in range(rows)}
dijkstra_previous = {(i, j): None for j in range(cols) for i in range(rows)}

# Variables for A* algorithm
astar_visited = set()
astar_distances = {(i, j): float('inf') for j in range(cols) for i in range(rows)}
astar_previous = {(i, j): None for j in range(cols) for i in range(rows)}

# Variables for DFS algorithm
dfs_visited = set()
dfs_previous = {(i, j): None for j in range(cols) for i in range(rows)}

# Variable to store the currently selected algorithm
current_algorithm = "Dijkstra"

def dijkstra():
    global start_point, end_point, dijkstra_visited, dijkstra_distances, dijkstra_previous

    heap = [(0, start_point)]
    dijkstra_distances[start_point] = 0

    while heap:
        current_distance, current_node = heapq.heappop(heap) # pop node with smallest distance from heap

        if current_node == end_point:
            break

        if current_node in dijkstra_visited:
            continue

        dijkstra_visited.add(current_node)

        for neighbor in get_neighbors(current_node):
            distance = current_distance + 1  # calculate distance, and Assuming each step has a distance of 1

            if distance < dijkstra_distances[neighbor]:
                dijkstra_distances[neighbor] = distance
                dijkstra_previous[neighbor] = current_node # updates distance and previous
                heapq.heappush(heap, (distance, neighbor)) 
                draw_grid()
                pygame.display.flip()

def astar():
    global start_point, end_point, astar_visited, astar_distances, astar_previous

    heap = [(0, start_point)]
    astar_distances[start_point] = 0

    while heap:
        current_distance, current_node = heapq.heappop(heap)

        if current_node == end_point:
            break

        if current_node in astar_visited:
            continue

        astar_visited.add(current_node)

        for neighbor in get_neighbors(current_node):
            distance = current_distance + 1  # Assuming each step has a distance of 1
            heuristic = math.sqrt((end_point[0] - neighbor[0]) ** 2 + (end_point[1] - neighbor[1]) ** 2)

            if distance < astar_distances[neighbor]:
                astar_distances[neighbor] = distance
                astar_previous[neighbor] = current_node
                heapq.heappush(heap, (distance + heuristic, neighbor)) # pushes next node into queue using distance + heuristic
                draw_grid()
                pygame.display.flip()

def dfs():
    global start_point, end_point, dfs_visited, dfs_previous

    stack = [(start_point, None)]
    while stack:
        current_node, previous_node = stack.pop() # pop current and previous node 
        if current_node in dfs_visited: 
            continue
        dfs_visited.add(current_node)
        dfs_previous[current_node] = previous_node
        if current_node == end_point:
            break
        for neighbor in get_neighbors(current_node):
            stack.append((neighbor, current_node)) # Push each neighbor onto the stack with the current node as its previous node
            draw_grid()
            pygame.display.flip()

def get_neighbors(node):
    i, j = node
    neighbors = []

    # Check the four cardinal directions R D L U
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for x, y in directions:
        new_i, new_j = i + x, j + y

        if 0 <= new_i < rows and 0 <= new_j < cols and grid[new_i][new_j] != -1:
            neighbors.append((new_i, new_j))

    return neighbors

# Function to draw the grid with colors
def draw_grid():
    screen.fill(pygame.Color("white"))  # Clear the screen

    for row in range(rows):
        for col in range(cols):
            if (row, col) == start_point:
                color = pygame.Color("blue")  # Start point
            elif (row, col) == end_point:
                color = pygame.Color("green")  # End point
            elif grid[row][col] == -1:
                color = pygame.Color("black")  # Wall
            elif current_algorithm == "Dijkstra":
                if (row, col) in dijkstra_visited and (row, col) != start_point and (row, col) != end_point:
                    color = pygame.Color("yellow")  # Visited node during Dijkstra's search
                elif (row, col) in get_shortest_path("Dijkstra"):
                    color = pygame.Color(255, 0, 0, 100)  # Shortest path with transparency for Dijkstra
                else:
                    color = pygame.Color("white")  # Empty cell
            elif current_algorithm == "A*":
                if (row, col) in astar_visited and (row, col) != start_point and (row, col) != end_point:
                    color = pygame.Color("yellow")  # Visited node during A* search
                elif (row, col) in get_shortest_path("A*"):
                    color = pygame.Color(255, 0, 0, 100)  # Shortest path with transparency for A*
                else:
                    color = pygame.Color("white")  # Empty cell
            elif current_algorithm == "DFS":
                if (row, col) in dfs_visited and (row, col) != start_point and (row, col) != end_point:
                    color = pygame.Color("yellow")  # Visited node during DFS search
                elif (row, col) in get_shortest_path("DFS"):
                    color = pygame.Color(255, 0, 0, 100)  # Shortest path with transparency for DFS
                else:
                    color = pygame.Color("white")  # Empty cell

            pygame.draw.rect(
                screen, color, (col * cell_size, row * cell_size, cell_size, cell_size)
            )
            pygame.draw.rect(
                screen, pygame.Color("black"), (col * cell_size, row * cell_size, cell_size, cell_size), 1
            )

    # Draw the text area background
    pygame.draw.rect(screen, pygame.Color("lightgray"), (width, 0, text_area_width, text_area_height))

    # Draw the text
    screen.blit(algorithm_text, (width + 10, 10))
    if current_algorithm == "DFS":
        nodes_visited_text = font.render(f"Nodes visited: {len(dfs_visited)}", True, pygame.Color("black"))
    else:
        nodes_visited_text = font.render(f"Nodes visited: {len(dijkstra_visited if current_algorithm == 'Dijkstra' else astar_visited)}", True, pygame.Color("black"))
    screen.blit(nodes_visited_text, (width + 10, 50))

def draw_shortest_path(algorithm):
    global end_point, dijkstra_previous, astar_previous, dfs_previous
    current_node = end_point
    if algorithm == "Dijkstra":
        previous = dijkstra_previous
    elif algorithm == "A*":
        previous = astar_previous
    else:
        previous = dfs_previous

    while current_node is not None:
        i, j = current_node
        pygame.draw.rect(
            screen, pygame.Color(255, 0, 0, 100), (j * cell_size, i * cell_size, cell_size, cell_size)
        )
        current_node = previous[current_node]

    # Draw the start and end points on top
    i, j = start_point
    pygame.draw.rect(
        screen, pygame.Color("blue"), (j * cell_size, i * cell_size, cell_size, cell_size)
    )

    i, j = end_point
    pygame.draw.rect(
        screen, pygame.Color("green"), (j * cell_size, i * cell_size, cell_size, cell_size)
    )

def get_shortest_path(algorithm):
    global end_point, dijkstra_previous, astar_previous, dfs_previous
    path = []
    current_node = end_point
    if algorithm == "Dijkstra":
        previous = dijkstra_previous
    elif algorithm == "A*":
        previous = astar_previous
    else:
        previous = dfs_previous

    while current_node is not None:
        path.append(current_node)
        current_node = previous[current_node]
    return path

# Function to reset the grid
def reset_grid():
    global grid, start_point, end_point, dijkstra_visited, dijkstra_distances, dijkstra_previous, astar_visited, astar_distances, astar_previous, dfs_visited, dfs_previous
    grid = [[0] * cols for _ in range(rows)]
    start_point = None
    end_point = None
    dijkstra_visited = set()
    dijkstra_distances = {(i, j): float('inf') for j in range(cols) for i in range(rows)}
    dijkstra_previous = {(i, j): None for j in range(cols) for i in range(rows)}
    astar_visited = set()
    astar_distances = {(i, j): float('inf') for j in range(cols) for i in range(rows)}
    astar_previous = {(i, j): None for j in range(cols) for i in range(rows)}
    dfs_visited = set()
    dfs_previous = {(i, j): None for j in range(cols) for i in range(rows)}

# Main loop
running = True
path_found = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // cell_size
            col = mouse_pos[0] // cell_size

            # Toggle between start point, end point, and wall on mouse click
            if grid[row][col] == 0 and start_point is None:
                grid[row][col] = 1  # Set as start point
                start_point = (row, col)
            elif grid[row][col] == 0 and end_point is None:
                grid[row][col] = 2  # Set as end point
                end_point = (row, col)
            elif grid[row][col] == -1:
                grid[row][col] = 0  # Remove wall
            elif grid[row][col] == 0 and start_point is not None and end_point is not None:
                grid[row][col] = -1  # Set as wall
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                current_algorithm = "Dijkstra"
                algorithm_text = font.render("Algorithm: Dijkstra", True, pygame.Color("black"))
            elif event.key == pygame.K_a:
                current_algorithm = "A*"
                algorithm_text = font.render("Algorithm: A*", True, pygame.Color("black"))
            elif event.key == pygame.K_s:
                current_algorithm = "DFS"
                algorithm_text = font.render("Algorithm: DFS", True, pygame.Color("black"))
            elif event.key == pygame.K_f and start_point is not None and end_point is not None:
                if current_algorithm == "Dijkstra":
                    dijkstra()
                elif current_algorithm == "A*":
                    astar()
                elif current_algorithm == "DFS":
                    dfs()
                path_found = True
            elif event.key == pygame.K_g:
                reset_grid()  # Reset the grid when "G" is pressed
                path_found = False

    draw_grid()

    if path_found:
        draw_shortest_path(current_algorithm)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()