import ciphers
import people

class Session:
    def __init__(self):
        self.implemented_ciphers = [ciphers.Caesar]
        self.sender = None
        self.reciver = None
        self.hacker = None
    
    def set_people(self):
        print("Welcome to this session!\nLet's set up the people using this service")
        print("These are the availible ciphers: ")
        _cipher = None
        while _cipher == None:
            i = 0
            for element in self.implemented_ciphers:
                print(str(i) + ": "+element.get_name(element))
                i += 1
            choice = input(">> ")
            try:
                _cipher = self.generate_cipher(int(choice))
            except TypeError:
                print("Invalid choice, try again")
        self.sender = people.Sender(_cipher)
        self.reciver = people.Reciver(_cipher)
        while True:
            print("Do you want a hacker? Y/N")
            _in = input(">> ")
            if _in == "Y":
                #self.hacker = people.Hacker(_cipher)
                break
            elif _in == "N":
                break
        print("Successfully set up!\n")

    def run(self):
        _continue = True
        while _continue:
            print("Please write a message: ")
            _message = input(">> ")
            print("Message recived. Encoding")
            _keys = self.sender.key
            _encoded = self.sender.operate_cipher(_message, _keys)
            print("Encoded message:" + _encoded + "\nWith key " + str(_keys))
            _decoded = self.reciver.operate_cipher(_encoded, _keys)
            if _message == _decoded:
                    print("Decoded sucessfully")
            else: print("Decoding failed")       
            print("Decoded message: " + _decoded+"\n")
            while True:
                print("Want to send another message? Y/N")
                _in = input(">> ")
                if _in == "Y":
                    break
                elif _in == "N":
                    _continue = False
                    break

    def generate_cipher(self, n):
        if n == 0:
            return ciphers.Caesar()

if __name__ == "__main__":
    current_session = Session()
    current_session.set_people()
    current_session.run()