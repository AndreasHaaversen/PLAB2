import calculator

class Session:
    def __init__(self):
        self.calc = calculator.Calculator()
    
    def run(self):
        _run = True
        print("Welcome to this calculator!\n")
        print("These operators are supported:")
        for element in self.calc.operators.keys():
            print(element)
        print("\nThese functions are supported:")
        for element in self.calc.functions.keys():
            print(element)
        print("\nPlease write everything exactly as described in the supported functions.")
        while _run:
            text = input("Your expression:\n>> ")
            result = self.calc.calculate_expression(text)
            print("Result: " + str(result))
            while True:
                print("\nWant to go again? Y/N")
                _in = input(">> ").upper()
                if _in == "Y":
                    break
                elif _in == "N":
                    _run = False
                    break

if __name__ == "__main__":
    session = Session()
    session.run()