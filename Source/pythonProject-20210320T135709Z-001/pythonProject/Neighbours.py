import copy

class Neighbours:


    def __init__(self):
        self.central = None
        self.cardinal = []
        self.ordinal = []

    def getstate(self):
        state = 0
        if self.central is not None:
            state += self.central.state
        if len(self.cardinal) > 0:
            state += sum(map(lambda _: _.state, self.cardinal))
        if len(self.ordinal) > 0:
            state += sum(map(lambda _: 0.83 * _.state, self.ordinal))
        return state


    def getall(self):
        all = []
        all.extend(copy.deepcopy(self.cardinal))
        all.extend(copy.deepcopy(self.ordinal))
        return all
