from abc import ABC, abstractmethod
import random
import math

class Cipher(ABC):
    
    def __init__(self):
        self.legal_ascii_lims = (32, 126)
        self.alphabet_size = self.legal_ascii_lims[1] - self.legal_ascii_lims[0]
        super(Cipher, self).__init__()

    @abstractmethod
    def encode(self, text, key):
        pass
    
    @abstractmethod
    def decode(self, text, key):
        pass
    
    @abstractmethod
    def generate_keys(self):
        pass
    
    def verify(self, text, key):
        return self.decode(self.encode(text, key),key) == text
    
    @abstractmethod
    def get_name(self):
        pass

class Caesar(Cipher):
    def __init__(self):
        self.__key_range = (1, 95)
        super(Caesar, self).__init__()

    def generate_keys(self):
        return random.randint(self.__key_range[0], self.__key_range[1])

    def encode(self, text, key):
        int_text = blocks_from_text(text)
        for i in range(0, len(int_text)):
            int_text[i] -= 32
            int_text[i] = (int_text[i] + key) % self.alphabet_size
            int_text[i] += 32
        return text_from_blocks(int_text)

    def decode(self, text, key):
        new_key = self.alphabet_size - key
        return self.encode(text, new_key)
    
    def get_name(self):
        return "Caesar cipher"

class Multiplication(Cipher):
    def __init__(self):
        super(Multiplication, self).__init__()
        self._valid_keys = self.set_keys()
    
    def set_keys(self):
        valid_keys = []
        for i in range(2,95):
            if(modular_inverse(i, self.alphabet_size)):
                valid_keys.append(i)
        return valid_keys
    
    def generate_keys(self):
        return self._valid_keys[random.randint(0,len(self._valid_keys))]

    def encode(self, text, key):
        if key in self._valid_keys:
            _int_text = blocks_from_text(text)
            for i in range(1, len(_int_text)):
                _int_text[i] -= 32
                _int_text[i] = (_int_text[i] * key) % self.alphabet_size
                _int_text[i] += 32
            return text_from_blocks(_int_text)
        else:
            print("Invalid key!")
    
    def decode(self, text, key):
        _inverse_key = modular_inverse(key, self.alphabet_size)
        return self.encode(text, _inverse_key)
    
    def get_name(self):
        return "Multiplication cipher"

class Affine(Cipher):
    def __init__(self):
        self.mult = Multiplication()
        self.caesar = Caesar()
        super(Affine, self).__init__()

    def generate_keys(self):
        return (self.mult.generate_keys(), self.caesar.generate_keys())
    
    def encode(self, text, key):
        return self.caesar.encode(self.mult.encode(text, key[0]), key[1])

    def decode(self, text, key):
        return self.mult.decode(self.caesar.decode(text, key[1]), key[0])

    def get_name(self):
        return "Affine cipher"

# Helpermethods
def modular_inverse(a, m):
    """
    Return the value x so that a*x = 1 (mod m) -- that is, so that a*x = k*m + 1 for some non-negative integer k.
    :param a: Value of a -- positive integer. This is the encoding key in the crypto-setting
    :param m: Value of m -- positive integer This is the length of the alphabet in the crypto-setting
    :return: Solution x -- positive integer.
    """

    def extended_gcd(_a, _b):
        """ Use the Extended Euclidean algorithm to calculate the "extended greatest common divisor".
        It takes as input two positive integers a and b, then calculates the following:
        1. The greatest common divisor (gcd) between a and b -- that is, the integer number g which is the largest
            integer for which a/g and b/g both are integers  (This can also be obtained using math.gcd)
        2. The integer x and y so that a*x + b*y = gcd(x, y)
        :param _a: Positive integer
        :param _b: Positive integer
        :return: Tuple (gcd, x, y)
        """
        previous_remainder, remainder = _a, _b
        current_x, previous_x, current_y, previous_y = 0, 1, 1, 0
        while remainder > 0:
            previous_remainder, (quotient, remainder) = remainder, divmod(previous_remainder, remainder)
            current_x, previous_x = previous_x - quotient * current_x, current_x
            current_y, previous_y = previous_y - quotient * current_y, current_y
        # The loop terminates with remainder == 0, x == b and y == -a. This is not what we want, and is because we have
        # walked it through one time "too many". Therefore, return the values of the previous round:
        return previous_remainder, previous_x, previous_y

    gcd_value, x, y = extended_gcd(a, m)
    if gcd_value != 1:
        #print('No inverse. gcd (%d, %d) is %d. Decoding is not unique. Choose another key than %d'
        #      % (a, m, math.gcd(a, m), a))
        return 0
    return x % m


def blocks_from_text(text, block_size = 1):
    """
    Converts a string message to a list of block integers. Each integer
    represents block_size characters in the text. Don't use too large a block_size, as that will give a *big* integer.
    Remember that if the generated unsigned int is larger than n in our key the decoding will not be unique.

    :param text: text message to be translated into blocks
    :param block_size: number of symbols/characters to be translated into one block
    :return: a list of integers; position <i> in the list is the integer representation of the i'th block of symbols
    """

    byte_representation = text.encode('utf_8')  # convert the string to bytes
    _blocks = []
    for start_position in range(0, len(byte_representation), block_size):
        this_block = int.from_bytes(byte_representation[start_position: min(start_position + block_size,
                                                                            len(text))], 'big', signed=False)
        _blocks.append(this_block)

    return _blocks


def text_from_blocks(blocks, no_bits = 1):
    """
    Converts a list of block integers to the original message string.
    blocks is the list of integers (generated by a call to blocks_from_text). no_bits is the number of bits
    used in the encryption, that is the no. bits used when generating the primes for the keys.

    :param blocks: a list of unsigned int's; typically the result of encoding the result of blocks_from_text()
    :param no_bits: the number of bits required to represent the integer in the byte-string
    :return: a string
    """
    _message = []
    for this_block in blocks:
        _message.append(this_block.to_bytes(
            2 * no_bits, byteorder='big', signed=False).decode(
            encoding='UTF-8', errors='ignore').lstrip('\0'))
    return ''.join(_message)

if __name__ == "__main__":
    cipher = Affine()
    print(cipher.verify("Hello World", cipher.generate_keys()))