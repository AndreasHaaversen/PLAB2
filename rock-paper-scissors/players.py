from abc import ABC, abstractmethod
from collections import defaultdict
import actions
import random

class Player(ABC):
    def __init__(self):
        self.actions =  {'Rock': 0, 'Scissors': 1, 'Paper': 2}
        super().__init__()
    
    @abstractmethod
    def choose_action(self):
        pass

    @abstractmethod
    def recive_result(self, own_action, other_action, winner):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

class randomPlayer(Player):

    def __init__(self):
        super().__init__()

    def choose_action(self):
        return actions.Action(random.randint(0, len(self.actions)))

    def recive_result(self, own_action, other_action, winner):
        pass
    
    def get_name(self):
        return "Random player"
    
class sequentialPlayer(Player):
    
    def __init__(self):
        super().__init__()
        self.lastAction = actions.Action(0)

    def choose_action(self):
        if self.lastAction.value + 1 == len(self.actions):
            index = 0
        else:
            index = self.lastAction.value + 1
        self.lastAction = actions.Action(index)
        return actions.Action(index)

    def recive_result(self, own_action, other_action, winner):
        pass
    
    def get_name(self):
        return "Sequential player"

class Most_Common(Player):

    def __init__(self):
        self.counts = defaultdict(int)
        super().__init__()

    def choose_action(self):
        if self.counts.keys() != []:
            common = max(self.counts.keys, key = (lambda x: self.counts[x]))
            beats_common = common.who_beats_me()
            return actions.Action(beats_common)
        else:
            return self.actions[random.randint(0, len(self.actions))]
    
    def recive_result(self, own_action, other_action, winner):
        self.counts[other_action] += 1

    def get_name(self):
        return "Most common player"

class Historian(Player):

    def __init__(self, husk):
        self.history = []
        self.husk = husk
        self.counts = defaultdict(int)
        super().__init__()

    def choose_action(self):
        if len(self.history) < self.husk + 1 or self.counts.keys() == [] or not self.history[0] in self.history[1:-1]:
            return self.actions[random.randint(0, len(self.actions))]
        else:
            possible = defaultdict(1)
            for tuples in self.counts.keys():
                if tuples[self.husk] == self.history[self.husk]:
                    possible[tuples] += 1
            common = max(possible.keys, key = (lambda x: possible[x]))
            beats_common = common.who_beats_me()
            return actions.Action(beats_common)

    def recive_result(self, own_action, other_action, winner):
        self.history.append(other_action)
        if len(self.history) >= self.husk + 1:
            for i in range(0, len(self.history), 3):
                self.counts[tuple(self.history[i:i + self.husk + 1])]
