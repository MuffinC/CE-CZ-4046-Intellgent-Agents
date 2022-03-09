'''
This file create the main core maze as acording to the image
Legend:
'#' = wall = 0
"+" = +1
"-" = -1
" " = white square = -0.04
'''
map = [['+', '#', '+', ' ', ' ', '+'],
       [' ', '-', ' ', '+', '#', '-'],
       [' ', ' ', '-', ' ', '+', ' '],
       [' ', ' ', ' ', '-', ' ', '+'],
       [' ', '#', '#', '#', '-', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ']
       ]
#task 2 requires a comples map instead, for this code i have created a map
#naturally, the altternative is to use it to be generated randomly
"""
1)Number of Forks leading into Dead Ends or Loops[I will implement dead ends]
2)Number of Forks along the correct path
3)Length of incorrect paths[total size will be 10x10]
4)Size of the maze [wont be explored, i will use the random maps to explore this]
5)Starting position changes [currently set to (9,0)]
"""
compli_map = [['+', '#', '+', '+', '+', '+', '-', '-', '-', '-'],
              ['+', '-', '+', '#', '#', '#', '#', '#', '#', '#'],
              ['-', '#', '#', '-', '-', '-', '+', ' ', '+', '-'],
              [' ', ' ', ' ', ' ', ' ', '#', '+', ' ', '+', '+'],
              [' ', '#', '#', '#', ' ', '-', ' ', ' ', '+', '+'],
              [' ', '#', ' ', ' ', ' ', '-', ' ', ' ', '+', '-'],
              [' ', '#', ' ', '#', '#', '#', '-', '#', '#', '#'],
              [' ', '#', ' ', '+', '+', '+', ' ', '#', '+', '+'],
              [' ', '#', '#', '#', '#', '#', '#', '#', '-', '-'],
              [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-'],
              ]

vars = ['+', '#', '-', '0']
#starting point for this is [3][2]
starting_p = { 'x': 3, 'y': 2 }

starting_p_compli = { 'x': 9, 'y': 0 }

# '#'is not needed in the legend, because it will just take up an aarray slot and will have no value

value_legend = {
    '+': 1,
    '-': -1,
    ' ': -0.04
}

RESULTS_DIR_PATH = 'assignment1/results/'

# for value iteration utilities to match reference utilities (approximately)
REFERENCE_DISCOUNT_FACTOR = 0.99
REFERENCE_MAX_ERROR = 1.4

# for value iteration
MAX_ERROR = 20

# for policy iteration
NUM_POLICY_EVALUATION = 100





