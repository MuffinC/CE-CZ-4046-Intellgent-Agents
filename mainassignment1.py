import copy
from pprint import pprint

from policies_algo import value_iteration, policy_iteration
from preset import *
from random_map import generate_maze
from maze import Maze, maze_movement
from plotter import plotter

def solve_MDP():
    """
    Main function.
    """
    # value iteration for task 1
    maze = Maze(
        grid=map,
        reward_mapping=value_legend,
        starting_point=starting_p,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    #show the current map, white spaces are represented by ' '
    for i in maze.grid:
        for j in i:
            print(j, end=" ")
        print()

    #run the maze through value iteration
    result = value_iteration(maze, max_error=MAX_ERROR)

    _show_maze_result(maze, result, 'map1_value_iteration_result.txt')

    # For approximation of reference utilities given in instructions,
    # use discount factor of 0.95 and maximum error threshold of 1.4. ideally, but since they
    #asked for 0.99 for discount factor we will use that
    # Values obtained through trial and error.
    maze = Maze(
        grid=map,
        reward_mapping=value_legend,
        starting_point=starting_p,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    result = value_iteration(maze, max_error=REFERENCE_MAX_ERROR)

    _show_maze_result(maze, result, 'map1_approximate_reference_utilities_result.txt')

    plotter(
        result['iteration_utilities'],
        save_file_name='map1_approximate_reference_utilities.png'
    )



    # policy iteration
    maze = Maze(
        grid=map,
        reward_mapping=value_legend,
        starting_point=starting_p,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    result = policy_iteration(maze, num_policy_evaluation=100)

    _show_maze_result(maze, result, 'map1_policy_iteration_result.txt')

    plotter(
        result['iteration_utilities'],
        save_file_name='map1_policy_iteration_utilities.png'
    )



    #We will now begin task 2 using a self derived complicated map
    maze = Maze(
        grid=compli_map,
        reward_mapping=value_legend,
        starting_point=starting_p_compli,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    #show the current map, white spaces are represented by ' '
    for i in maze.grid:
        for j in i:
            print(j, end=" ")
        print()

    #run the maze through value iteration
    result = value_iteration(maze, max_error=MAX_ERROR)

    _show_maze_result(maze, result, 'compli_map_value_iteration_result.txt')

    # For approximation of reference utilities given in instructions,
    # use discount factor of 0.95 and maximum error threshold of 1.4.
    # Values obtained through trial and error.
    maze = Maze(
        grid=compli_map,
        reward_mapping=value_legend,
        starting_point=starting_p_compli,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    result = value_iteration(maze, max_error=REFERENCE_MAX_ERROR)

    _show_maze_result(maze, result, 'compli_map_approximate_reference_utilities_result.txt')

    plotter(
        result['iteration_utilities'],
        save_file_name='compli_map_approximate_reference_utilities.png'
    )
    # policy iteration
    maze = Maze(
        grid=compli_map,
        reward_mapping=value_legend,
        starting_point=starting_p_compli,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    result = policy_iteration(maze, num_policy_evaluation=100)

    _show_maze_result(maze, result, 'compli_map_policy_iteration_result.txt')

    plotter(
        result['iteration_utilities'],
        save_file_name='compli_map_policy_iteration_utilities.png'
    )




    # This next portion is for the random analysis, to see the results of a larger maze with a
    #starting position of task 1
    #edit here to change bonus maze dimensions. now it will generate a 100x100 square
    bonus_grid_length = 100
    bonus_grid = generate_maze(bonus_grid_length)

    print('bonus grid, length =', bonus_grid_length)
    with open(RESULTS_DIR_PATH + 'bonus_maze.txt', 'w') as file:
        pprint(bonus_grid, file)

    #this is on the assumption that we are not changing the starting position
    bonus_maze = Maze(
        grid=bonus_grid,
        reward_mapping=value_legend,
        starting_point=starting_p,
        discount_factor=REFERENCE_DISCOUNT_FACTOR
    )
    for i in bonus_maze.grid:
        for j in i:
            print(j, end=" ")
        print()

    #repeat the same processes as task 1 just that now with the bonus maze
    result = value_iteration(bonus_maze, max_error=MAX_ERROR, verbose=True)

    _show_maze_result(
        bonus_maze,
        result,
        'bonus_value_iteration_result.txt'
    )

    plotter(
        result['iteration_utilities'],
        'bonus_value_iteration_utilities.png'
    )

    result = policy_iteration(bonus_maze, NUM_POLICY_EVALUATION, verbose=True)

    _show_maze_result(
        bonus_maze,
        result,
        'bonus_policy_iteration_result.txt'
    )

    plotter(
        result['iteration_utilities'],
        'bonus_policy_iteration_utilities.png'
    )



def _show_maze_result(maze, result, save_file_name=None):
    """
    params:
    - maze (Maze)
    - result (dict): result of solving a maze
    - save_file_name (str): name of file to save plot as; defaults to None (not saved)
    """
    lines = []

    line = 'number of iterations required: ' + str(result['num_iterations'])
    print(line)
    lines.append(line)

    utilities, optimal_policy = result['utilities'], result['optimal_policy']

    optimal_policy_grid = copy.deepcopy(maze.grid)
    action_symbol_map = {
        maze_movement.MOVE_UP: '∧',
        maze_movement.MOVE_DOWN: 'v',
        maze_movement.MOVE_LEFT: '<',
        maze_movement.MOVE_RIGHT: '>',
    }

    line = '---utility for each state (row, column)---'
    print(line)
    lines.append(line)

    for state_position in maze.states:
        if state_position[1] == 0:
            print()

        line = str(state_position) + ' - utility: {:.3f}'.format(utilities[state_position])
        print(line)
        lines.append(line)

        action = optimal_policy[state_position]
        action_symbol = action_symbol_map[action]

        optimal_policy_grid[state_position[0]][state_position[1]] = action_symbol

    line = '---optimal policy grid (w = wall)---'
    print(line)
    lines.append(line)

    for i in optimal_policy_grid:
        for j in i:
            print(j, end=" ")
        print()

    if save_file_name is not None:
        with open(RESULTS_DIR_PATH + save_file_name, 'w') as file:
            for line in lines:
                file.write(line + '\n')
            #pprint(optimal_policy_grid, file)


if __name__ == '__main__':
    solve_MDP()