class Action:
    __valid_actions = {'Rock': 0, 'Scissors': 1, 'Paper': 2}

    def __init__(self, val):
        if isinstance(val, str):
            val = self.__valid_actions[val]
        assert isinstance(val, int) & (val >= 0) & (val < len(self.__valid_actions))
        self.value = val

    def __eq__(self, other):
        return self.value == other.value
    
    def __gt__(self, other):
        return (len(self.__valid_actions) + other.value - self.value) % len(self.__valid_actions) == 1

    def __str__(self):
        return list(self.__valid_actions.keys())[self.value]

    def who_beats_me(self):
        return (self.value - 1) % len(self.__valid_actions)
