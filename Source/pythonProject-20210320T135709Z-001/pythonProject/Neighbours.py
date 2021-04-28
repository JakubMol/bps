import copy
from scipy.special import softmax
class Neighbours:


    def __init__(self):
        self.central = None
        self.cardinal = []
        self.ordinal = []

    def getstatenotopography(self):
        state = 0
        if self.central is not None:
            state += self.central.state
        if len(self.cardinal) > 0:
            state += sum(map(lambda _: _.state, self.cardinal))
        if len(self.ordinal) > 0:
            state += sum(map(lambda _: 0.83 * _.state, self.ordinal))
        return state

    def getstate(self):
        state = 0
        if self.central is not None:
            state += self.central.state
        if len(self.cardinal) > 0:
            state += sum(map(lambda _: _.state * (((self.central.elevation - _.elevation) / self.sum() if self.sum() > 0 else 1)), self.cardinal))
        if len(self.ordinal) > 0:
            state += sum(map(lambda _: 0.83 * _.state * (((self.central.elevation - _.elevation) / self.sum() if self.sum() > 0 else 1)), self.ordinal))
        return state


    def getall(self):
        all = []
        all.extend(copy.deepcopy(self.cardinal))
        all.extend(copy.deepcopy(self.ordinal))
        return all

    def sum(self):
        all = copy.deepcopy(self.getall())
        all.append(self.central)
        return sum(_.elevation for _ in all)

