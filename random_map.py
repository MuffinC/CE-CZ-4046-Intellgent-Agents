import random
import pprint

#Assuming we need to retain the same orientation as the given maze for the random mazr
# 16/36 = 71.11% is not white spaces
# Among non-white spaces (16 squares), roughly
# ~1/3 are walls (5 walls),
# ~1/3 are brown squares (5 brown),
# ~1/3 are green squares (6 green)

def generate_maze(grid_length: int):
    """
    Generates a maze as a square grid that has size of (grid_length x grid_length).

    params:
    - grid_length (int): length of the grid

    return:
    - 2D array (list of list): [
        [' ', ..., ' '],
        ...,
        [' ', ..., ' '],
    ]
    """
    random.seed()
    grid = []

    for row in range(grid_length):
        grid.append([])

        for _ in range(grid_length):  # _ is column; column value not used
            #random assignment of colour value
            colour_number = random.random()

            #to follow the same % of walls
            if colour_number < 0.5 / 3:
                grid[row].append('#')  # wall

            elif colour_number < 0.5 * 2 / 3:
                grid[row].append('-')  # -1

            elif colour_number < 0.5:
                grid[row].append('+')  # +1

            else:
                grid[row].append(' ')  # whitespace -0.04

    return grid