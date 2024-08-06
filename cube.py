import time
import curses

def draw_line(stdscr, x0, y0, x1, y1):
    """Draw a line using Bresenham's line algorithm"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        try:
            # Draw point
            stdscr.addstr(y0, x0, '#')
            stdscr.refresh()
            time.sleep(0.01)
        except curses.error:
            pass
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def project(x, y, z):
    """Project 3D coordinates onto 2D plane"""
    c = 3   # Add 3 to z to work around Devide-By-Zero
    factor = 25 / (z + c)  # Change to scale up and down
    new_x = int(x * factor + 50)  # Terminal width 100
    new_y = int(-y * factor + 25)  # Terminal height 50
    return new_x, new_y

def print_cube(stdscr, vertices):
    """Print the cube on the screen"""
    # Define the cube's edges by connecting vertices
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    for edge in edges:
        start_vertex = vertices[edge[0]]
        end_vertex = vertices[edge[1]]
        start_x, start_y = project(*start_vertex)
        end_x, end_y = project(*end_vertex)
        try:
            draw_line(stdscr, start_x, start_y, end_x, end_y)
        except curses.error:
            pass

def main(stdscr):
    # Hide cursor
    curses.curs_set(0)

    # Define cube dimensions
    width = 2  # Width of the cube
    height = 2  # Height of the cube
    depth = 2  # Depth of the cube

    # Calculate half dimensions for convenience
    half_width = width / 2
    half_height = height / 2
    half_depth = depth / 2

    # Define initial cube vertices
    vertices = [
        (-half_width, -half_height, -half_depth),   # 0 - left bottom front
        (half_width, -half_height, -half_depth),    # 1 - right bottom front
        (half_width, half_height, -half_depth),     # 2 - right top front
        (-half_width, half_height, -half_depth),    # 3 - left top front
        (-half_width, -half_height, half_depth),    # 4 - left bottom back
        (half_width, -half_height, half_depth),     # 5 - right bottom back
        (half_width, half_height, half_depth),      # 6 - right top back
        (-half_width, half_height, half_depth)      # 7 - left top back
    ]

    # Draw cube loop
    while 1:
        stdscr.clear()

        print_cube(stdscr, vertices)

        stdscr.refresh()
        time.sleep(3)  # Adjust speed of rotation

if __name__ == "__main__":
    curses.wrapper(main)