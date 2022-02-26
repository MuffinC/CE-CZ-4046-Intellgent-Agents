"""
Purpose of this file is just to declare abstraction models that willl be defined
during the process itself
"""
class mdp1:
    def __init__(self, states, actions, discount):

        self.states = states
        self.actions = actions
        self.discount = discount

    def transition_model(self, state, action, next_state) -> float:
        """
        This is just to get the p of moving to the next state,given S and A at current
        """
        pass

    def reward_function(self, state):
        """
        returns: the reward obtained at current state
        """
        pass

    def get_next_states(self, state, action):
        """
        params:
        - state (tuple): x, y position
        - action (MazeAction): action to take at the given state
        return: possible next states
        """
        pass
