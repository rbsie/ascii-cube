import time
import curses

def draw_edge(stdscr, x0, y0, x1, y1):
    """Use bresenham's algorithm to draw an edge"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        try:
            # Draw dot in terminal
            stdscr.addstr(y0, x0, '#') # y value first!!!
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
    """Project 3D coordinates onto 2D plane and scale to terminal size"""
    # Define terminal size
    width = 100
    height = 50
    
    factor = 20 # Change to scale up and down 
    z += 5   # Translate z away from (0, 0, 0) to avoid Devide-By-Zero

    # Devide by z because camera is at (0, 0, 0)
    new_x = int((x * factor) / z)
    new_y = int((-y * factor) / z)

    # Center in terminal window
    new_x += int(width / 2)
    new_y += int(height / 2)

    return new_x, new_y

def print_cube(stdscr, vertices):
    """Print cube in terminal"""
    # Define edges by connecting vertices
    vectors = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
        ]

    for vector in vectors:
        tail_vertex = vertices[vector[0]]
        head_vertex = vertices[vector[1]]
        tail_x, tail_y = project(*tail_vertex)
        head_x, head_y = project(*head_vertex)
        try:
            draw_edge(stdscr, tail_x, tail_y, head_x, head_y)
        except curses.error:
            pass

def main(stdscr):
    # Hide cursor
    curses.curs_set(False)

    # Define cube dimensions (even numbers only!)
    width = 4
    height = 4
    depth = 4

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
        time.sleep(3)   # Refresh rate

if __name__ == "__main__":
    curses.wrapper(main)