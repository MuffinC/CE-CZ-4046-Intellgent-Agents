"""
Algorithm for both
-Value Iteration
-Policy Iteration

"""

from markovdec_abstract import mdp1
from maze import maze_movement


def value_iteration(mdp: mdp1,max_error=1,verbose=False,):
    """
    relies on bellman equation as an update rule to give a "value" to all squares
    :param mdp:
    standard algo
    State s=(x,y)
    Action given state = A(s)
    Transition model = P(s'|s,a)
    Reward, R, given state s, R(s)
    discount gamma =

    :param max_error:max allowed in util of a state
    :param verbose: just to print data

    :return:
        'utilities': {
            (x, y): utility value (float)
        },
        'optimal_policy': {
            (x, y): best action to take at this state [maze_movement]
        },
        'num_iterations': num_iterations (int)[total iterations made]
        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    """

    #state data
    cur_data ={}
    new_data ={}
    iteration_data ={}

    #the best policy
    optimal ={}

    # starting the algo
    convergence = False
    num_iterations = 0

    #initialization of states from defined data
    for state_x in mdp.states:

        cur_data[state_x] = 0
        new_data[state_x] = 0
        optimal[state_x] = None

        # creating multiple empty lists to be filled based on states preset
        iteration_data[state_x] = []

    #Algo

    while not convergence:
        for state_x in mdp.states:
            cur_data[state_x] = new_data[state_x]  # U ← U′
            iteration_data[state_x].append(cur_data[state_x])

        max_utility_change = 0  # δ ← 0

        # for each state s in S do
        for state_x in mdp.states:
            # U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]
            new_utility, new_action = bellman(mdp,state_x,cur_data,)

            new_data[state_x] = new_utility
            optimal[state_x] = new_action

            # if |U′[s]−U[s]| > δ then δ ← |U′[s]−U[s]|
            abs_utility_difference = abs(new_data[state_x] - \
                                         cur_data[state_x])

            if abs_utility_difference > max_utility_change:
                max_utility_change = abs_utility_difference

        num_iterations += 1

        if verbose:
            print(
                'iteration:', num_iterations,
                '-maximum change in the utility of any state:',
                '{:.6f}'.format(max_utility_change),
            )

        # until δ < ϵ(1−γ)/γ
        convergence = max_utility_change < \
                        max_error * (1 - mdp.discount) / mdp.discount


    return{
        'utilities': cur_data,
        'optimal_policy': optimal,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_data,
    }
def expected_util(mdp: mdp1,state_x: tuple, action: maze_movement,util: dict, )->float:
    """
    Implementation of ∑s′P(s′|s, a)U[s′]
    params:
    - mdp (MarkovDecisionProcess): the MDP to solve
    - state_position (tuple): x, y
    - action (MazeAction): action to take at the given state
    - utilities: {
        (x, y): utility value (float)
    }
    return: utility value of the state given (float)
    """
    expected_util = 0

    possible_next_states = mdp1.get_next_states(state_x, action)

    for intended_next_state_position in possible_next_states:
        # The intended state to move into is used (even if it is invalid).
        # If there are more than 1 wall / border surrounding current state,
        # there will be an overlap in next states, since they will end up
        # remaining in the current state.

        # If next_state_1 == next_state_2, the transition model defined
        # will fail to calculate the correct probability, so intended state
        # is used instead of actual state
        probability = mdp.transition_model(
            state_x,
            action,
            intended_next_state_position
        )

        # actual state used to calculate utility,
        # since intended state may be invalid (wall / out of bounds)
        actual_next_state_position = \
            possible_next_states[intended_next_state_position]['actual']
        next_state_utility = util[actual_next_state_position]

        expected_util += probability * next_state_utility

    return expected_util

def bellman (mdp: mdp1,state_x: tuple, cur_data: dict):
    """
    Implementation of U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]

    params:
    - MDP to solve
    - state_position (tuple): x, y
    - cur_data (dict): maps any (x, y) to its current utility value

    return: (
        updated utility value of the state given (float),
        best action to take at the state given (Maze_movement),
    )
    """

    max_expected_utility = float('-inf')
    best_action = None

    action_next_state_map = mdp.states[state_x]

    for action in action_next_state_map:
        expected_utility = expected_util(
            mdp,
            state_x,
            action,
            cur_data
        )

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

    # U′[s] next predicted utility
    return (
        mdp.reward_function(state_x) + mdp.discount * max_expected_utility,
        best_action,
    )













