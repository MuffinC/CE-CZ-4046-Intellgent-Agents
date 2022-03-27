#File just to get the analysis for the 2 polocies and the 2 different mazes
#imports
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

value_headers = ['State', 'Iteration', 'Utility']
#policy has action
policy_headers = ['State', 'Iteration', 'Action', 'Utility']

"""
just change the name in the csv write/read
Complicated_maze_analysis_policy_it.csv
Complicated_maze_analysis_value_it.csv
Normal_maze_analysis_policy_it.csv
Normal_maze_analysis_value_it.csv

Random_maze_analysis_value_it.csv
Random_maze_analysis_policy_it.csv
"""

value_df = pd.read_csv('Complicated_maze_analysis_value_it.csv', names = value_headers, index_col='State')
policy_df = pd.read_csv('Complicated_maze_analysis_policy_it.csv', names = policy_headers, index_col='State')

def analysis(vorp,pos):
    if vorp == 0:
        value_state_df = value_df.loc[pos]
        return value_state_df
    else:
        policy_state_df = policy_df.loc[pos]
        return policy_state_df

# change the values to 9 and 9 for the 10x10 complicated maze
colsize= 9
rowsize= 9
positions =[]

for x in range(0,colsize+1):
    for y in range(0,rowsize+1):
        stringcall = ",".join(str(x)+str(y))
        stringcall="("+stringcall +")"
        positions.append(stringcall)
        stringcall =""

figure(figsize=(16, 8))

for x in positions:
    value_state_df = analysis(0,x)
    plt.plot(value_state_df['Iteration'], value_state_df['Utility'], label=x)
plt.title("Value Iteration vs Utility Scores [Complicated Maze]")
plt.xlabel("Iterations")
plt.ylabel("Utility Values")
plt.legend(loc=2, prop={'size': 6})
plt.savefig("Value Iteration vs Utility Scores [Complicated Maze].png")
plt.show()

figure(figsize=(16, 8))
for x in positions:
    policy_state_df = analysis(1,x)
    plt.plot(policy_state_df['Iteration'], policy_state_df['Utility'], label=x)
plt.title("Policy Iteration vs Utility Scores [Complicated Maze]")
plt.xlabel("Iterations")
plt.ylabel("Utility Values")
plt.legend(loc=2, prop={'size': 6})
plt.savefig("Policy Iteration vs Utility Scores [Complicated Maze].png")
plt.show()

