from abc import ABC, abstractmethod

class Cipher(ABC):
    __legal_alphabet = [chr(i) for i in range(32,127)]
    __alpahet_size = len(__legal_alphabet)
    __encode_key = None
    __decode_key = None
    __possible_keys = None

    @abstractmethod
    def encode(self, text, key):
        pass
    
    @abstractmethod
    def decode(self, text, key):
        pass
    
    def verify(self, text, key):
        return self.decode(self.encode(text, key),key) == text

