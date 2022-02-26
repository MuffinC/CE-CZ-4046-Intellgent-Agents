'''
This file create the main core maze as acording to the image
Legend:
'#' = wall = 0
"+" = +1
"-" = -1
"S" = Start
" " = white square = -0.04
'''
map = [['+', '#', '+', ' ', ' ', '+'],
       [' ', '-', ' ', '+', '#', '-'],
       [' ', ' ', '-', ' ', '+', ' '],
       [' ', ' ', 'S', '-', ' ', '+'],
       [' ', '#', '#', '#', '-', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ']
       ]
vars = ['+', '#', '-', '0']
#starting point for this is [3][2]
starting_p = { 'x': 3, 'y': 2 }



value_legend = {
    '+': 1,
    '#': 0,
    '-': -1,
    'S': 0,
    ' ': -0.04
}

RESULTS_DIR_PATH = 'assignment_1/results/'

# for value iteration utilities to match reference utilities (approximately)
REFERENCE_DISCOUNT_FACTOR = 0.99
REFERENCE_MAX_ERROR = 1.4

# for value iteration
MAX_ERROR = 20

# for policy iteration
NUM_POLICY_EVALUATION = 100





