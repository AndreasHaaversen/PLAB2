from abc import ABC, abstractclassmethod
import numbers


class Container(ABC):

    def __init__(self):
        self._items = []
        super(Container, self).__init__()
    
    def is_empty(self):
        return len(self._items) == 0
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self, position):
        assert not self.is_empty()
        return self._items.pop(position)
    
    def peek(self, position):
        assert not self.is_empty()
        return self._items[position]
    
    def size(self):
        return len(self._items)
    
    def clear(self):
        self._items.clear()
    
class Stack(Container):
    def __init__(self):
        super(Stack, self).__init__()
    
    def pop(self, position = -1):
        return super(Stack, self).pop(position)
    
    def peek(self, position = -1):
        return super(Stack, self).peek(position)
    
class Queue(Container):
    def __init__(self):
        super(Queue, self).__init__()
    
    def peek(self, position = 0):
        return super(Queue, self).peek(position)
    
    def pop(self, position = 0):
        return super(Queue, self).pop(position)
    
class Function:
    def __init__(self, func):
        self.func = func
    
    def execute(self, element, debug = False):
        if not isinstance(element, numbers.Number):
            raise TypeError("Cannot execute function on the given argument: " + str(element))
        result = self.func(element)
        if debug == True:
            print("Function: " + self.func.__name__ + "({:f}) = {:f}".format(element, result))
        return result
    
class Operator:
    def __init__(self, op, strength):
        self.op = op
        self.strength = strength

    def execute(self, e1, e2, debug = False):
        if not (isinstance(e1, numbers.Number) or isinstance(e2, numbers.Number)):
            raise TypeError("Invalid aguments given to operator: " + str((e1,e2)))
        result = self.op(e1, e2)
        if debug == True:
            print("Operator: " + self.op.__name__ + "({:f}, {:f}) = {:f}".format(e1, e2, result))
        return result