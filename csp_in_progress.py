class Problem(object):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def result(self, state, action):
        raise NotImplementedError

    def value(self, state):
        raise NotImplementedError

   
