from abc import ABC, abstractclassmethod

class Person(ABC):
    def __init__(self, cipher):
        self.cipher = cipher
        self.key = cipher.generate_keys()
    
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
    
    def operate_cipher(self, text, key):
        out = self.cipher.encode(text, key)
        self.set_key(self.cipher.generate_keys())
        return out

class Reciver(Person):
    def __init__(self, cipher):
        super(Reciver, self).__init__(cipher)
    
    def operate_cipher(self, text, key):
        return self.cipher.decode(text, key)

class Hacker(Person):
    # TODO: Implemnt this class
    pass