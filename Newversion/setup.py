import random
'''
This file create the main core maze as acording to the image
Legend:
'#' = wall = 0
"+" = +1
"-" = -1
" " = white square = -0.04
"S" = starting position
'''

"""
map = [['+', '#', '+', ' ', ' ', '+'],
       [' ', '-', ' ', '+', '#', '-'],
       [' ', ' ', '-', ' ', '+', ' '],
       [' ', ' ', 'S', '-', ' ', '+'],
       [' ', '#', '#', '#', '-', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ']
       ]
"""
#starting point for this is [3][2]
def initialise(inti):
    #inti is just if it is value iteration or policy iteration
    # inti = 0 = value iteration
    if inti == 0:
        START = (3, 2)
        #encoding the map into matrix form
        Rewards = [(0,0),(0,2), (0,5), (1,3), (2,4), (3,5)]  # +
        loss = [(1,1), (1,5), (2,2), (3,3), (4,4)] # -
        wall = [(0,1), (1,4), (4,1), (4,2), (4,3)] # #
        rows = 6
        columns = 6
        gamma =0.99
        reward_val = -0.04
        eps = 10**(-2) # needs to be like this if not will cause float not iterable error
        return START,reward_val,Rewards,loss,wall,rows,columns,gamma,eps

    else:
        # task 2 requires a comples map instead, for this code i have created a map
        # naturally, the altternative is to use it to be generated randomly
        """
        1)Number of Forks leading into Dead Ends or Loops[I will implement dead ends]
        2)Number of Forks along the correct path
        3)Length of incorrect paths[total size will be 10x10]
        4)Size of the maze [wont be explored, i will use the random maps to explore this]
        5)Starting position changes [currently set to (9,0)]
        """

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
                      ['S', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-'],
                      ]

        """
        START = (9, 0)
        # encoding the map into matrix form
        Rewards = [(0, 0), (0, 2), (0, 3), (0, 4), (0, 5),
                   (1, 0), (1, 2),
                   (2, 6), (2, 8),
                   (3, 6), (3, 8), (3, 9),
                   (4, 8), (4, 9),
                   (5, 8),
                   (7, 3), (7, 4), (7, 5), (7, 7), (7, 8), (7, 9)]  # +

        loss = [(0, 6), (0, 7), (0, 8), (0, 9),
                (1, 1),
                (2, 0), (2, 3), (2, 4), (2, 5), (2, 9),
                (4, 5),
                (5, 5), (5, 9),
                (6, 6),
                (8, 8), (8, 9),
                (9, 9)]  # -

        wall = [(0, 1),
                (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
                (2, 1), (2, 2),
                (3, 5),
                (4, 1), (4, 2), (4, 3),
                (5, 1),
                (6, 1), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8), (6, 9),
                (7, 1), (7, 7),
                (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), ]  # #
        rows = 10
        columns = 10
        gamma = 0.99
        eps = 10 ** (-2)
        reward_val = -0.04
        return START, reward_val, Rewards, loss, wall, rows, columns, gamma, eps

def randomizer(grid_length):
    rows = grid_length
    columns = grid_length
    gamma = 0.99
    eps = 10 ** (-2)
    reward_val = -0.04

    random.seed()
    wall =[]
    Rewards = []
    loss = []
    star =0

    for x in range(grid_length):
        for y in range(0,grid_length):
            wheel = random.random()
            if wheel < 0.5 / 3:
                wall.append((x,y))  # wall
            elif wheel < 0.5 * 2 / 3:
                loss.append((x,y))  # -1
            elif wheel < 0.5:
                Rewards.append((x,y))  # +1
            else:
                if star == 0:
                    star=1
                    START = (x, y)
                continue
    print(wall)
    print(Rewards)
    print(loss)
    return START, reward_val, Rewards, loss, wall, rows, columns, gamma, eps












