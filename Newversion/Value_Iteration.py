#imports
import copy
import csv
from Reusable_fn import truncate
from setup import randomizer
#initialise setup first
NUM_ACTIONS = 4
ACTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up Left Down Right (WASD)
START,reward_val,REWARD,BAD_RE,walls,rowst,columnst,gamma,eps = randomizer(30) #change 0 -> to 1 for the complicated maze or change it to Randomizer(grid_length)

"""
just change the name in the csv write/read
Complicated_maze_analysis_policy_it.csv
Complicated_maze_analysis_value_it.csv
Normal_maze_analysis_policy_it.csv
Normal_maze_analysis_value_it.csv

Random_maze_analysis_value_it.csv
Random_maze_analysis_policy_it.csv
"""
#creating the environment
#Initialise blank values first

environment = [ [0] * columnst for i in range(rowst)]
# input the rewards and bad rewards
for coord in REWARD:
    environment[coord[0]][coord[1]] = 1
for coord in BAD_RE:
    environment[coord[0]][coord[1]] = -1

def print_environment(environment):
    #this is to just show the outcome's of the iterations in command line
    display = ""
    for row in range(rowst):
        display += "|"
        for col in range(columnst):
            if (row, col) in walls:
                val = "WALL"
            elif (row, col) in REWARD:
                val = "+1"
            elif (row, col) in BAD_RE:
                val = "-1"
            else:
                val = str(environment[row][col])
            display += " " + val[:5].ljust(5) + " |"
        display += "\n"
    print(display)

def print_policy(policy):
    # prints out the best policy for the current state in command line
    display = ""
    for row in range(rowst):
        display += "|"
        for col in range(columnst):
            if (row, col) in walls:
                val = "WALL"
            elif START != None and (row,col) == START:
                val = "S" + " (" + ["↑", "←", "↓", "→"][policy[row][col]] + ")"
            elif (row, col) in REWARD:
                val = "+1" + " (" + ["↑", "←", "↓", "→"][policy[row][col]] + ")"
            elif (row, col) in BAD_RE:
                val = "-1" + " (" + ["↑", "←", "↓", "→"][policy[row][col]] + ")"
            else:
                val = ["↑", "←", "↓", "→"][policy[row][col]]
            display += " " + val[:6].ljust(6) + " |"
        display += "\n"
    print(display)

def get_utility(environment, row, col, action):
    #just a function to get thee current utility values out
    change_row, change_col = ACTIONS[action]
    new_row = row + change_row
    new_col = col + change_col

    if new_row < 0 or new_row >= rowst or new_col < 0 or new_col >= columnst \
        or (new_row, new_col) in walls:
        return environment[row][col]
    else:
        return environment[new_row][new_col]


def calculate_utility(environment, row, col, action):
    #Calculator function, to get the new utility values
    # utiltiy = REWARD
    if (row, col) in REWARD:
        utility = 1
    elif (row, col) in BAD_RE:
        utility = -1
    else:
        utility = reward_val
    utility += 0.1 * gamma * get_utility(environment, row, col, (action - 1) % 4)
    utility += 0.8 * gamma * get_utility(environment, row, col, action)
    utility += 0.1 * gamma * get_utility(environment, row, col, (action + 1) % 4)

    return utility


def value_iteration(environment, isAnalyze):
    if isAnalyze:
        with open('Random_maze_analysis_value_it.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            #open csv to store data there, easier to refer
            # Initial values are all 0
            for row in range(rowst):
                for col in range(columnst):
                    writer.writerow([f"({row},{col})", 0, 0])
            iteration = 1
            while True:
                print(f"Iteration {iteration}")

                next_env = copy.deepcopy(environment)
                error = 0
                for row in range(rowst):
                    for col in range(columnst):
                        # Bellman update
                        next_env[row][col] = max(
                            [calculate_utility(environment, row, col, action) for action in range(NUM_ACTIONS)])
                        error = max(error, abs(next_env[row][col] - environment[row][col]))
                        writer.writerow([f"({row},{col})", iteration, truncate(next_env[row][col], 3)])

                environment = next_env

                print_environment(environment)
                if error < eps  * (1 - gamma) / gamma:
                    break
                iteration += 1
    else:
        iteration = 1
        while True:
            print(f"Iteration {iteration}")
            next_env = copy.deepcopy(environment)
            error = 0
            for row in range(rowst):
                for col in range(columnst):
                    # Bellman update
                    # implementation of bellman equation
                    # U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]
                    # or
                    # V*(s) = max ∑T(s,a,s')*[R(s,a,s') + γ V*(s')]
                    next_env[row][col] = max(
                        [calculate_utility(environment, row, col, action) for action in range(NUM_ACTIONS)])
                    error = max(error, abs(next_env[row][col] - environment[row][col]))
            # If the expected utility of the action is higeher than the current max utility, assign it as the new max util
            # this is to get the max value as a result

            environment = next_env
            #return new iteration count
            print_environment(environment)
            if error < eps * (1 - gamma) / gamma:
                break
            iteration += 1

    return environment


def get_optimal_policy(environment):
    policy = [[-1] * columnst for i in range(rowst)]

    for row in range(rowst):
        for col in range(columnst):

            # Select action that maximizes utility 
            max_action = None
            max_utility = -float("inf")

            for action in range(NUM_ACTIONS):
                utility = calculate_utility(environment, row, col, action)
                if utility > max_utility:
                    max_action = action
                    max_utility = utility
            policy[row][col] = max_action

    # return  optimal policy
    # for policy extraction step
    return policy




isAnalyze = True

if isAnalyze:
    #to get the utility values for analysis
    with open('Random_maze_analysis_value_it.csv', 'w', newline='') as file:
        writer = csv.writer(file)

print(environment)
print(f"Displaying initial policy")
print_environment(environment)

environment = value_iteration(environment, isAnalyze)

optimal_policy = get_optimal_policy(environment)

# Displaying the Optimal Policy
print(f"Optimal policy through Value Iteration is")
print_policy(optimal_policy)