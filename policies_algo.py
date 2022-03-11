"""
Algorithm for both
-Value Iteration
-Policy Iteration

"""

from markovdec_abstract import MDP
from maze import maze_movement


def value_iteration(mdp: MDP,max_error=1,verbose=False):
    """
    relies on bellman equation as an update rule to give a "value" to all squares
    :param mdp:
    standard algo
    State s=(x,y)
    Action given state = A(s)
    Transition model = P(s'|s,a)
    Reward, R, given state s, R(s)
    discount gamma =γ, used for expected future result
    :param max_error:max allowed in util of a state
    :param verbose: just to print data

    :return:
        Utilities is the utility value of the (x,y) position
        'utilities': {
            (x, y): utility value (float)
        },

        optimal policy will be then used for policy extraction, second part of value iteration
        for the givevn (x,y) square
        'optimal_policy': {
            (x, y): best action to take at this state [maze_movement]
        },

        Total iterations made for the whole operation
        'num_iterations': num_iterations (int)[total iterations made]

        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    """

    #base state data=0 for iteration 0
    cur_data ={}
    new_data ={}
    iteration_data ={}

    #the best policy
    optimal ={}

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
        #run until convergence

        for state_x in mdp.states:
            cur_data[state_x] = new_data[state_x]  # Load the new state into the current one,
            iteration_data[state_x].append(cur_data[state_x]) #

        max_utility_change = 0  # δ ← 0

        # for each state s in S do
        for state_x in mdp.states:
            #implementation of bellman equation
            # U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]
            # or
            # V*(s) = max ∑T(s,a,s')*[R(s,a,s') + γ V*(s')]
            new_utility, new_action = bellman(mdp,state_x,cur_data,)

            new_data[state_x] = new_utility
            optimal[state_x] = new_action

            # if |U′[s]−U[s]| > δ then δ ← |U′[s]−U[s]|

            abs_utility_difference = abs(new_data[state_x] - cur_data[state_x])

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
        convergence = max_utility_change < max_error * (1 - mdp.discount) / mdp.discount

    #return both value iteration outcome and optimal policy
    # for policy extraction step and also the number of iterations
    return{
        'utilities': cur_data,
        'optimal_policy': optimal,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_data,
    }
def expected_util(mdp: MDP,state_x: tuple, action: maze_movement,util: dict, )->float:
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

    possible_next_states = mdp.get_next_states(state_x, action)

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

def bellman (mdp: MDP,state_x: tuple, cur_data: dict):
    """
    Implementation of U′[s] ← R(s) + γ max a∈A(s) ∑s′P(s′|s, a)U[s′]
    V*(s) = max ∑T(s,a,s') [R(s,a,s')+ γ V*(s')]

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
        #If the expected utility of the action is higeher than the current max utility, assign it as the new max util
        #this is to get the max value as a result
        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

    # V*(s) value
    return (
        mdp.reward_function(state_x) + mdp.discount * max_expected_utility,
        best_action,
    )

"""
policy iteration
"""
def policy_iteration(mdp: MDP, num_policy_evaluation: int=1,verbose: bool=False):
    """
    params:
    - mdp (MarkovDecisionProcess): an MDP with
        states S,
        actions A(s),
        transition model P(s′|s, a),
        rewards R(s),
        discount γ
    - num_policy_evaluation (int): number of times to do policy evaluation (k)
    - verbose (bool): determines whether to print information

    return: {
        'utilities': {
            (x, y): utility value (float)
        },
        'optimal_policy': {
            (x, y): best action to take at this state (MazeAction)
        },
        'num_iterations': num_iterations (int),
        'iteration_utilities': {
            (x, y): [utility for each iteration (float)]
        }
    }
    """
    # U , a vector of utilities for states in S , initially zero
    # π, a policy vector indexed by state, initially random
    utilities, policy = {}, {}

    # for: Plot of utility estimates as a function of the number of iterations
    iteration_utilities = {}

    for state_position in mdp.states:
        utilities[state_position] = 0
        policy[state_position] = maze_movement.MOVE_UP

        # start with first utility in place since it is updated at end of iteration
        iteration_utilities[state_position] = [0]

    unchanged = False
    num_iterations = 0

    # repeat
    while not unchanged:
        # U ← POLICY-EVALUATION (π, U , mdp)
        utilities, new_iteration_utilities = _policy_evaluation(
            mdp,
            policy,
            utilities,
            num_policy_evaluation,
        )

        policy, unchanged = _policy_improvement(mdp, policy, utilities)

        num_iterations += num_policy_evaluation
        print('unchanged:', unchanged, 'at iteration:', num_iterations)

        if verbose:
            print('iteration:', num_iterations)

        for state_position in mdp.states:
            iteration_utilities[state_position].extend(new_iteration_utilities[state_position])

            if verbose:
                print('at', state_position, '-best action:', policy[state_position])

    # algorithm: return π
    #
    # in my implementation, I return the utilities and number of iterations
    # as well, as they will come in useful later
    return {
        'utilities': utilities,
        'optimal_policy': policy,
        'num_iterations': num_iterations,
        'iteration_utilities': iteration_utilities,
    }


def _policy_evaluation(
        mdp: MDP,
        policy: dict,
        utilities: dict,
        num_policy_evaluation: int,
):
    """
    Simplified version of Bellman equation.

    params:
    - mdp (MarkovDecisionProcess): an MDP with
        states S,
        actions A(s),
        transition model P(s′|s, a),
        rewards R(s),
        discount γ
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }
    - num_policy_evaluation (int): number of times to do policy evaluation (k)

    return: (
        { (x, y): updated utility value (float) },
        { (x, y): [utility for each iteration (float)] }
    )
    """
    current_utilities, updated_utilities = {}, {}
    new_iteration_utilities = {}

    for state_position in mdp.states:
        # U_i ← U
        current_utilities[state_position] = utilities[state_position]
        new_iteration_utilities[state_position] = []

    # for i in range(k)
    for _ in range(num_policy_evaluation):
        # for each state s in S do
        for state_position in mdp.states:
            reward = mdp.reward_function(state_position)

            # ∑s′P (s'|s, π_i(s)) U_i(s')
            expected_utility = expected_util(
                mdp,
                state_position,
                policy[state_position],
                current_utilities
            )

            # U_i+1(s) ← R(s) + γ ∑s′P (s'|s, π_i(s)) U_i(s')
            updated_utilities[state_position] = reward + mdp.discount * expected_utility

        # U_i ← U_i+1
        for state_position in mdp.states:
            current_utilities[state_position] = updated_utilities[state_position]
            new_iteration_utilities[state_position].append(current_utilities[state_position])

    return (current_utilities, new_iteration_utilities)


def _policy_improvement(
        mdp,
        policy,
        utilities,
):
    """
    params:
    - mdp (MarkovDecisionProcess): the MDP to solve
    - policy: {
        (x, y): best action to take at this state (MazeAction)
    }
    - utilities: {
        (x, y): utility value (float)
    }

    return: (
        updated_policy (dict),
        unchanged (bool),
    )
    """
    updated_policy = {}
    unchanged = True  # unchanged? ← true

    # for each state s in S do
    for state_position in mdp.states:
        # get max a∈A(s) ∑s′ P (s'|s, a) U [s']
        max_expected_utility = float('-inf')
        best_action = None

        action_next_state_map = mdp.states[state_position]

        for action in action_next_state_map:
            expected_utility = expected_util(
                mdp,
                state_position,
                action,
                utilities
            )

        if expected_utility > max_expected_utility:
            max_expected_utility = expected_utility
            best_action = action

        # get ∑s′ P (s'|s, π[s]) U [s']
        utility = expected_util(
            mdp,
            state_position,
            policy[state_position],
            utilities
        )

        # if max a∈A(s) ∑s′ P (s'|s, a) U [s'] > ∑s′ P (s'|s, π[s]) U [s'] then do
        if max_expected_utility > utility:
            updated_policy[state_position] = best_action
            unchanged = False
        else:
            updated_policy[state_position] = policy[state_position]

    return (updated_policy, unchanged)











