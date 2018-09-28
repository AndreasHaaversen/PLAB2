import calculator_utils as CUT
import numbers
import numpy

class Calculator:
    def __init__(self):
        self.functions = {'EXP': CUT.Function(numpy.exp),
                          'LOG': CUT.Function(numpy.log),
                          'SIN': CUT.Function(numpy.sin),
                          'COS': CUT.Function(numpy.cos),
                          'SQRT': CUT.Function(numpy.sqrt)}
        
        self.operators = {'PLUSS': CUT.Operator(numpy.add, 0),
                          'MINUS': CUT.Operator(numpy.subtract, 0),
                          'GANGE': CUT.Operator(numpy.multiply, 1),
                          'DELE': CUT.Operator(numpy.divide, 1)}

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
                while (not self.operator_stack.is_empty()) and (isinstance(self.operator_stack.peek(), CUT.Function) or (isinstance(self.operator_stack.peek(), CUT.Operator) and element.strength < self.operator_stack.peek().strength)):
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.push(element)
            else:
                raise TypeError('Cannot recognize element while converting to RPN')
        while not self.operator_stack.is_empty():
            self.output_queue.push(self.operator_stack.pop())