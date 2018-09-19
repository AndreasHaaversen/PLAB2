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
    def recive_result(self, own_action, other_action):
        pass
    
    @abstractmethod
    def get_name(self):
        pass

class randomPlayer(Player):

    def __init__(self):
        super().__init__()

    def choose_action(self):
        return actions.Action(random.randint(0, 2))

    def recive_result(self, own_action, other_action):
        pass
    
    def get_name(self):
        return "Random player"
    
class sequentialPlayer(Player):
    
    def __init__(self):
        self.lastAction = actions.Action(0)
        super().__init__()

    def choose_action(self):
        if self.lastAction.value + 1 == len(self.actions):
            index = 0
        else:
            index = self.lastAction.value + 1
        self.lastAction = actions.Action(index)
        return actions.Action(index)

    def recive_result(self, own_action, other_action):
        pass
    
    def get_name(self):
        return "Sequential player"

class Most_Common(Player):

    def __init__(self):
        self.counts = {"Rock": 0, "Scissors": 0, "Paper": 0}
        super().__init__()

    def choose_action(self):
        action = actions.Action(max(self.counts, key=lambda key: self.counts[key]))
        return actions.Action(action.who_beats_me())
    
    def recive_result(self, own_action, other_action):
        self.counts[str(other_action)] += 1

    def get_name(self):
        return "Most common player"

class Historian(Player):

    def __init__(self, husk = 3):
        self.husk_sequence = [None] * husk
        self.husk = husk
        self.counts = {}
        super().__init__()

    def choose_action(self):
        if tuple(self.husk_sequence) in self.counts:
            next_action = actions.Action(max(self.counts[tuple(self.husk_sequence)], key = lambda key:self.counts[tuple(self.husk_sequence)][key]))
            return actions.Action(next_action.who_beats_me())
        else:
            return actions.Action(random.randint(0, 2))

    def recive_result(self, own_action, other_action):
        if not (tuple(self.husk_sequence) in self.counts):
            self.counts[tuple(self.husk_sequence)] = {"Rock": 0, "Scissors": 0, "Paper": 0}
        self.counts[tuple(self.husk_sequence)][str(other_action)] += 1
        self.husk_sequence.append(str(other_action))
        self.husk_sequence.pop(0)
    
    def get_name(self):
        return "Historian"
