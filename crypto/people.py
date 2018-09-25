from abc import ABC, abstractclassmethod
from collections import defaultdict

class Person(ABC):
    def __init__(self, cipher):
        self.cipher = cipher
        self.key = None
    
    def set_key(self, key):
        self.key = key
    
    def get_key(self):
        return self.key

    @abstractclassmethod
    def operate_cipher(self, text, key):
        pass

class Sender(Person):
    def __init__(self, cipher):
        super(Sender, self).__init__(cipher)
        self.set_key(self.cipher.generate_keys())

    
    def operate_cipher(self, text, key):
        out = self.cipher.encode(text, key)
        return out

class Reciver(Person):
    def __init__(self, cipher):
        super(Reciver, self).__init__(cipher)

    
    def operate_cipher(self, text, key):
        return self.cipher.decode(text, key)

class Hacker(Person):
    def __init__(self, cipher):
        self._valid_words = self.load_words()
        self.hit_dict = defaultdict(int)
        super(Hacker, self).__init__(cipher)
    
    def operate_cipher(self, text, key = None):
        _valid_keys = self.cipher.get_valid_keys()
        _valid_keys.remove("")
        for aKey in _valid_keys:
            _decoded_text = self.cipher.decode(text, aKey).lower().split()
            for word in _decoded_text:
                if word in self._valid_words:
                    self.hit_dict[aKey] += 1
        
        best_key = max(self.hit_dict, key=lambda key: self.hit_dict[key])
        out = self.cipher.decode(text, best_key)
        print("The hacker belives it has found a valid key!")
        print("It found key " + str(best_key) + ", with text:\n"+out)
        self.hit_dict = defaultdict(int)

    def load_words(self):
        out = set()
        with open('english_words.txt', 'r') as file:
            for line in file:
                out.add(line.rstrip())
        return out