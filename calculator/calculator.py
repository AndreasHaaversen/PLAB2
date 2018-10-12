import calculator_utils as CUT
import numbers
import numpy
import re

class Calculator:
    def __init__(self):
        self.functions = {'EXP': CUT.Function(numpy.exp),
                          'LOG': CUT.Function(numpy.log),
                          'SIN': CUT.Function(numpy.sin),
                          'COS': CUT.Function(numpy.cos),
                          'SQRT': CUT.Function(numpy.sqrt),
                          'TAN': CUT.Function(numpy.tan)}
        
        self.operators = {'PLUSS': CUT.Operator(numpy.add, 0),
                          'MINUS': CUT.Operator(numpy.subtract, 0),
                          'GANGE': CUT.Operator(numpy.multiply, 1),
                          'DELE': CUT.Operator(numpy.divide, 1),
                          'MOD': CUT.Operator(numpy.mod, 1),
                          'RAISE': CUT.Operator(numpy.power, 2)}

        self.output_queue = CUT.Queue()
        self.operator_stack = CUT.Stack()

    def eval_RPN(self):
        while not self.output_queue.is_empty():
            element = self.output_queue.pop()
            if isinstance(element, numbers.Number):
                self.operator_stack.push(element)
            elif isinstance(element, CUT.Function):
                num = self.operator_stack.pop()
                self.operator_stack.push(element.execute(num))
            elif isinstance(element, CUT.Operator):
                n1 = self.operator_stack.pop()
                n2 = self.operator_stack.pop()
                self.operator_stack.push(element.execute(n2,n1))
            else:
                raise TypeError('Could not recognize stack element as a valid type!')
        return self.operator_stack.pop()

    def convert_to_RPN(self, elements):
        for element in elements:
            if isinstance(element, numbers.Number):
                self.output_queue.push(element)
            elif isinstance(element, CUT.Function):
                self.operator_stack.push(element)
            elif element == '(':
                self.operator_stack.push(element)
            elif element == ')':
                while self.operator_stack.peek() != '(':
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.pop()
            elif isinstance(element, CUT.Operator):
                while (not self.operator_stack.is_empty()) and (isinstance(self.operator_stack.peek(), CUT.Function) 
                        or (isinstance(self.operator_stack.peek(), CUT.Operator) and element.strength < self.operator_stack.peek().strength)):
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.push(element)
            else:
                raise TypeError('Could not recognize element while converting to RPN: ' +str(element))
        while not self.operator_stack.is_empty():
            self.output_queue.push(self.operator_stack.pop())
        
    def parse_text(self, text):
        out = []
        text = text.replace(" ", "").upper()
        func_targets = "|".join(["^" + func for func in self.functions.keys()])
        op_targets = "|".join(["^" + op for op in self.operators.keys()])
        while len(text) > 0:
            check = re.search("^[-0123456789.]+", text)
            if check != None:
                out.append(float(check.group(0)))
                text = text[check.end(0):]
            check1 = re.search(func_targets, text)
            if check1 != None:
                out.append(self.functions[check1.group(0)])
                text = text[check1.end(0):]
            check2 = re.search(op_targets, text)
            if check2 != None:
                out.append(self.operators[check2.group(0)])
                text = text[check2.end(0):]
            check3 = re.search("^\\(", text)
            if check3 != None:
                out.append(check3.group(0))
                text = text[check3.end(0):]
            check4 = re.search("^\\)", text)
            if check4 != None:
                out.append(check4.group(0))
                text = text[check4.end(0):]
            check5 = re.search("^PI", text)
            if check5 != None:
                out.append(numpy.pi)
                text = text[check5.end(0):]
            if check == None and check1 == None and check2 == None and check3 == None and check4 == None and check5 == None:
                print("Could not interpet input.\n\nExiting...")
                exit()
        return out
    
    def calculate_expression(self, text):
        elements = self.parse_text(text)
        self.convert_to_RPN(elements)
        return self.eval_RPN()