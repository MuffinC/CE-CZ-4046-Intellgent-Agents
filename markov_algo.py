class markov:
    #declaration of items in markov decision process
    def __init__(self,states,action,prob,reward):
        self.states = states
        self.action = action
        self.prob = prob
        self.reward = reward
