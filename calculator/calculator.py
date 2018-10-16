import calculator_utils as CUT
import numbers
import numpy
import re

class Calculator:
    def __init__(self):

        # All supported functions
        self.functions = {'EXP': CUT.Function(numpy.exp),
                          'LOG': CUT.Function(numpy.log),
                          'SIN': CUT.Function(numpy.sin),
                          'COS': CUT.Function(numpy.cos),
                          'SQRT': CUT.Function(numpy.sqrt),
                          'TAN': CUT.Function(numpy.tan)}
        
        # All supported operators
        self.operators = {'PLUSS': CUT.Operator(numpy.add, 0),
                          'MINUS': CUT.Operator(numpy.subtract, 0),
                          'GANGE': CUT.Operator(numpy.multiply, 1),
                          'DELE': CUT.Operator(numpy.divide, 1),
                          'MOD': CUT.Operator(numpy.mod, 1),
                          'RAISE': CUT.Operator(numpy.power, 2)}

        self.output_queue = CUT.Queue()
        self.operator_stack = CUT.Stack()

    def eval_RPN(self):
        # We still have elements to process
        while not self.output_queue.is_empty():

            element = self.output_queue.pop()

            # Numbers go straigth to the operator stack
            if isinstance(element, numbers.Number):
                self.operator_stack.push(element)
            
            # Functions pop a number from the operator stack, executes with it and returns the result to the operator stack
            elif isinstance(element, CUT.Function):
                num = self.operator_stack.pop()
                self.operator_stack.push(element.execute(num))
            
            # Operators pop two numbers from the operator stack, and executes with them. The result is pushed back onto the operator stack
            elif isinstance(element, CUT.Operator):
                n1 = self.operator_stack.pop()
                n2 = self.operator_stack.pop()
                self.operator_stack.push(element.execute(n2,n1))
            
            # The world is ending
            else:
                raise TypeError('Could not recognize stack element as a valid type!')

        # We are done! The last element on the stack is the result
        return self.operator_stack.pop()

    def convert_to_RPN(self, elements):
        for element in elements:

            # These are simple tests for elements that should go directly onto either the output stack or op queue
            if isinstance(element, numbers.Number):
                self.output_queue.push(element)
            elif isinstance(element, CUT.Function):
                self.operator_stack.push(element)
            elif element == '(':
                self.operator_stack.push(element)

            # We found a closing parentesis, we now have to move all the ops onto the output queue and reomve the opening parentesis
            elif element == ')':
                while self.operator_stack.peek() != '(':
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.pop()

            # We found an operator!
            # We now have to move all functions and operators with higher strength onto the output queue
            elif isinstance(element, CUT.Operator):
                while (not self.operator_stack.is_empty()) and (isinstance(self.operator_stack.peek(), CUT.Function) 
                        or (isinstance(self.operator_stack.peek(), CUT.Operator) and element.strength < self.operator_stack.peek().strength)):
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.push(element)

            # Something has gone terribly wrong if we end up here
            else:
                raise TypeError('Could not recognize element while converting to RPN: ' +str(element))
            
        # We are done. Move all the remaining elements on the operator stack onto the output queue
        while not self.operator_stack.is_empty():
            self.output_queue.push(self.operator_stack.pop())
        

    def parse_text(self, text):
        out = []
        text = text.replace(" ", "").upper()
        # Create regex-targets for the functions and the operators
        func_targets = "|".join(["^" + func for func in self.functions.keys()])
        op_targets = "|".join(["^" + op for op in self.operators.keys()])

        # We still have text to parse
        while len(text) > 0:

            check = re.search("^[-0123456789.]+", text)
            # Did we find a number? If so, add to out and splice remaining text
            if check != None:
                out.append(float(check.group(0)))
                text = text[check.end(0):]

            check1 = re.search(func_targets, text)
            # Did we find a function?
            if check1 != None:
                out.append(self.functions[check1.group(0)])
                text = text[check1.end(0):]

            check2 = re.search(op_targets, text)
            # Did we find an operator?
            if check2 != None:
                out.append(self.operators[check2.group(0)])
                text = text[check2.end(0):]

            check3 = re.search("^\\(", text)
            # Did we find a opening parenthesis?
            if check3 != None:
                out.append(check3.group(0))
                text = text[check3.end(0):]

            check4 = re.search("^\\)", text)
            # Did we find a closing parenthesis?
            if check4 != None:
                out.append(check4.group(0))
                text = text[check4.end(0):]

            check5 = re.search("^PI", text)
            # Did we find PI?
            if check5 != None:
                out.append(numpy.pi)
                text = text[check5.end(0):]

            # Did we find anything at all?
            if check == None and check1 == None and check2 == None and check3 == None and check4 == None and check5 == None:
                print("Could not interpet input.\n\nExiting...")
                exit()
        return out
    
    def calculate_expression(self, text):
        elements = self.parse_text(text)
        self.convert_to_RPN(elements)
        return self.eval_RPN()