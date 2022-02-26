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
starting_p = (3,2)
value_legend = {
    '+': 1,
    '#': 0,
    '-': -1,
    'S': 0,
    ' ': -0.04
}
discount =0.99
possible_actions =[
    
]


