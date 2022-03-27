#imports
import csv
import copy
from Reusable_fn import truncate
from setup import randomizer
#creating the environment
#Initialise blank values first
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

environment = [ [0] * columnst for i in range(rowst)]
# input the rewards and bad rewards
for coord in REWARD:
    environment[coord[0]][coord[1]] = 1
for coord in BAD_RE:
    environment[coord[0]][coord[1]] = -1

fixed_action = 0 # Up (0) Left (1) Down (2) Right (3) (WASD)
policy = [[fixed_action] * columnst for i in range(rowst)]

#Same functions as value iteration

def print_environment(environment):
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


# Prints out the given policy (reccommended action at each state)
def print_policy(policy):
    display = ""
    for row in range(rowst):
        display += "|"
        for col in range(columnst):
            if (row, col) in walls:
                val = "WALL"
            elif START != None and (row, col) == START:
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
    change_row, change_col = ACTIONS[action]
    new_row = row + change_row
    new_col = col + change_col

    if new_row < 0 or new_row >= rowst or new_col < 0 or new_col >= columnst \
            or (new_row, new_col) in walls:
        return environment[row][col]
    else:
        return environment[new_row][new_col]

def calculate_utility(environment, row, col, action):
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


# Performs evaluation of the current policy and make improvements if any
def policy_evaluation(policy, environment, iteration, isAnalyze):
    error = 0
    while True:
        next_env = copy.deepcopy(environment)
        error = 0
        for row in range(rowst):
            for col in range(columnst):
                next_env[row][col] = calculate_utility(environment, row, col, policy[row][col])
                error = max(error, abs(next_env[row][col] - environment[row][col]))

        environment = next_env
        if error < eps * (1 - gamma) / gamma:
            break

    if isAnalyze:
        with open('Random_maze_analysis_policy_it.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for row in range(rowst):
                for col in range(columnst):
                    writer.writerow([f"({row},{col})", iteration, policy[row][col], truncate(environment[row][col], 3)])

    # print_environment(environment)
    return environment


def policy_iteration(policy, environment, isAnalyze):
    iteration = 1
    while True:
        environment = policy_evaluation(policy, environment, iteration, isAnalyze)
        is_changed = False
        for row in range(rowst):
            for col in range(columnst):
                max_action = None
                max_utility = -float("inf")
                for action in range(NUM_ACTIONS):
                    utility = calculate_utility(environment, row, col, action)
                    if utility > max_utility:
                        max_action = action
                        max_utility = utility

                if max_utility > calculate_utility(environment, row, col, policy[row][col]):
                    policy[row][col] = max_action
                    is_changed = True

        if is_changed:
            print(f"Iteration {iteration}")
            print_policy(policy)

        if is_changed == False:
            break

        iteration += 1

    return policy


#write data to csv
isAnalyze = True
if isAnalyze:
    with open('Random_maze_analysis_policy_it.csv', 'w', newline='') as file:
        writer = csv.writer(file)

# Dispalying the Inital Policy
print(f"Displaying initial policy")
print_policy(policy)

# Policy Iteration
policy = policy_iteration(policy, environment, isAnalyze)

# Displaying the Optimal Policy
print(f"Optimal policy through Policy Iteration is")
print_policy(policy)
