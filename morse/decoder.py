import serial # This is the key import so that we can access the serial port.

# Codes for the 5 signals sent to this level from the Arduino

_dot = 1
_dash = 2
_symbol_pause = 3
_word_pause = 4
_reset = 5

# Morse Code Class
class morseDecoder():

# Note: the codes for dot and dash coming to Python via the serial port are 1 and 2, respectively, since those were most
# convenient at the Arduino level. However, I've switched to 0 and 1 in this dictionary, since it is a lot easier to
# read.  So O = dot, 1 = dash in the _morse_codes dictionary below.  You will need to remember that when looking
# up letters and digits in this dictionary.

    _morse_codes = {'01':'a','1000':'b','1010':'c','100':'d','0':'e','0010':'f','110':'g','0000':'h','00':'i','0111':'j',
               '101':'k','0100':'l','11':'m','10':'n','111':'o','0110':'p','1101':'q','010':'r','000':'s','1':'t',
               '001':'u','0001':'v','011':'w','1001':'x','1011':'y','1100':'z','01111':'1','00111':'2','00011':'3',
               '00001':'4','00000':'5','10000':'6','11000':'7','11100':'8','11110':'9','11111':'0'}



    # Static method
    @staticmethod
    def connect():
        for i in range(100):
            try:
                arduino = serial.Serial('COM' + str(i), 9600, timeout=.1)
                print("Connected to arduino")
                return arduino
            except serial.SerialException:
                pass
        exit("Arduino was not found")

    #Instance methods
	# This is where you set up the connection to the serial port.
    def __init__(self,sport=True):
        if sport:
            self.serial_port = self.connect()
        self.reset()

    def reset(self):
        self.current_message = ''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 1-4 from the Arduino via a serial port
    def read_one_signal(self,port=None):
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data
                
    # The signal returned by the serial port is one (sometimes 2) bytes, that represent characters of a string.  So,
    # a 2 looks like this: b'2', which is one byte whose integer value is the ascii code 50 (ord('2') = 50).  The use
    # of function 'int' on the string converts it automatically.   But, due to latencies, the signal sometimes
    # consists of 2 ascii codes, hence the little for loop to cycle through each byte of the signal.

    def decoding_loop(self):
        while True:
            s = self.read_one_signal(self.serial_port)
            print(s)
            for byte in s:
                self.process_signal(int(chr(byte)))

    def process_signal(self, sig):
        if(sig == _dot):
            self.current_symbol += '0'
        elif(sig == _dash):
            self.current_symbol += '1'
        elif(sig == _symbol_pause):
            try:
                self.current_word += self._morse_codes[self.current_symbol]
                print(self._morse_codes[self.current_symbol])
            except KeyError:
                print(self.current_symbol + " Is not a valid key")
            self.current_symbol = ''
        elif(sig == _word_pause):
            self.symbolCleanup()
            self.current_message += self.current_word + ' '
            print(self.current_word)
            self.current_word = ''
        else:
            self.symbolCleanup()
            self.current_message += self.current_word
            print(self.current_message)
            print("\nMessage recived. System is resetting")
            self.reset()

    def symbolCleanup(self):
        if(self.current_symbol != ''):
            try:
                self.current_word += self._morse_codes[self.current_symbol]
                self.current_symbol = ''
            except KeyError:
                print("Unable to parse current symbol")

def main():
    decoder = morseDecoder()
    print("Welcome to the morse decoder!")
    #print("The system will start momentarly. Please wait.")
    decoder.decoding_loop()

main()