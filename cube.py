import curses
import time
import math

def rotate(x_angle, y_angle, z_angle, x, y, z):
    '''Rotates vector around x, y, z axes by given angles'''
    # Rotate around x
    first_x = x
    first_y = y * math.cos(x_angle) + z * (-math.sin(x_angle))
    first_z = y * math.sin(x_angle) + z * math.cos(x_angle)

    # Rotate around y
    second_x = first_x * math.cos(y_angle) + first_z * math.sin(y_angle)
    second_y = first_y
    second_z = first_x * (-math.sin(y_angle)) + first_z * math.cos(y_angle)

    # Rotate around z
    third_x = second_x * math.cos(z_angle) + second_y * (-math.sin(z_angle))
    third_y = second_x * math.sin(z_angle) + second_y * math.cos(z_angle)
    third_z = second_z

    return third_x, third_y, third_z


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
    # see: https://stackoverflow.com/questions/724219/how-to-convert-a-3d-point-into-2d-perspective-projection/724243#724243
    new_x = int((x * factor) / z)
    new_y = int((-y * factor) / z)

    # Center in terminal window
    new_x += int(width / 2)
    new_y += int(height / 2)

    return new_x, new_y

def draw_cube(stdscr, vertices):
    """Draw cube in terminal"""
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

    # Define initial cube vertices around (0, 0, 0)
    vertices = [
        (-half_width, -half_height, -half_depth),   # 0 - l b f
        (half_width, -half_height, -half_depth),    # 1 - r b f
        (half_width, half_height, -half_depth),     # 2 - r t f
        (-half_width, half_height, -half_depth),    # 3 - l t f
        (-half_width, -half_height, half_depth),    # 4 - l b b
        (half_width, -half_height, half_depth),     # 5 - r b b
        (half_width, half_height, half_depth),      # 6 - r t b
        (-half_width, half_height, half_depth)      # 7 - l t b
    ]

    x_angle, y_angle, z_angle = 0, 0, 0
    factor = 0

    # Draw cube loop
    while 1:
        stdscr.clear()

        rotated_vertices = []

        for vertex in vertices:
            rotated_vertex = rotate(x_angle, y_angle, z_angle, *vertex)
            rotated_vertices.append(rotated_vertex)

        draw_cube(stdscr, rotated_vertices)
        stdscr.refresh()

        # Combining multiple sine and cosine waves with different frequencies and amplitudes gives a rich,
        # harmonized rotational effect
        x_angle = math.sin(0.01 * factor) * 40 + math.cos(0.005 * factor) * 30
        y_angle = math.sin(0.015 * factor) * 50 + math.cos(0.01 * factor) * 20
        z_angle = math.sin(0.02 * factor) * 60 + math.cos(0.02 * factor) * 10

        factor += 0.1

        time.sleep(0.05)   # Refresh rate

if __name__ == "__main__":
    curses.wrapper(main)