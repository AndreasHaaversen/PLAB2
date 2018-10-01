import calculator_utils
import calculator
import numpy
import unittest
import numbers

class TestCalculator(unittest.TestCase):
    def test_containers(self):
        s1 = calculator_utils.Stack()
        q1 = calculator_utils.Queue()
        s1.push(1)
        s1.push(2)
        self.assertEqual(2, s1.peek())
        self.assertEqual(2, s1.pop())
        self.assertEqual(1, s1.peek())
        self.assertEqual(1, s1.pop())
        q1.push(1)
        q1.push(2)
        self.assertEqual(1, q1.peek())
        self.assertEqual(1, q1.pop())
        self.assertEqual(2, q1.peek())
        self.assertEqual(2, q1.pop())

    def test_functions(self):
        exp = calculator_utils.Function(numpy.exp)
        log = calculator_utils.Function(numpy.log)
        self.assertAlmostEqual(exp.execute(5), numpy.exp(5))
        self.assertAlmostEqual(exp.execute(-5), numpy.exp(-5))
        self.assertAlmostEqual(log.execute(2), numpy.log(2))
        self.assertRaises(TypeError, exp, 'potet')
        self.assertRaises(TypeError, log, 'potet')

    def test_operators(self):
        plus = calculator_utils.Operator(numpy.add, 1)
        minus = calculator_utils.Operator(numpy.subtract,1)
        mult = calculator_utils.Operator(numpy.multiply,2)
        div = calculator_utils.Operator(numpy.divide,2)
        self.assertEqual(20, mult.execute(4,5))
        self.assertEqual(5, plus.execute(2,3))
        self.assertEqual(-5, minus.execute(4,9))
        self.assertEqual(2, div.execute(4,2))
        self.assertEqual(15, mult.execute(5, div.execute(9,3)))

    def test_calculator(self):
        calc = calculator.Calculator()
        self.assertAlmostEqual(1096.6331584284585, calc.functions['EXP'].execute(calc.operators['PLUSS'].execute(1, calc.operators['GANGE'].execute(2, 3))))
        calc.output_queue.push(1)
        calc.output_queue.push(2)
        calc.output_queue.push(3)
        calc.output_queue.push(calculator_utils.Operator(numpy.multiply, 1))
        calc.output_queue.push(calculator_utils.Operator(numpy.add, 0))
        calc.output_queue.push(calculator_utils.Function(numpy.exp))
        self.assertAlmostEqual(1096.6331584284585, calc.eval_RPN())

    def test_shunting_yard(self):
        calc = calculator.Calculator()
        list1_of_ops = [2, calc.operators['GANGE'], 3, calc.operators['PLUSS'], 1]
        calc.convert_to_RPN(list1_of_ops)
        self.assertEqual(7, calc.eval_RPN())
        list2_of_ops = [calc.functions['EXP'], '(', 1, calc.operators['PLUSS'], 2, calc.operators['GANGE'], 3, ')']
        calc.convert_to_RPN(list2_of_ops)
        self.assertAlmostEqual(1096.63315843, calc.eval_RPN())

    def test_text_parser(self):
        calc = calculator.Calculator()
        ex1 = [2.0, calc.operators['GANGE'], 3.0, calc.operators['PLUSS'], 1.0]
        txt1 = "2.0 GANGE 3.0 PLUSS 1.0"
        self.assertEqual(ex1, calc.parse_text(txt1))
        ex2 = [calc.functions['EXP'], '(', 1.0, calc.operators['PLUSS'], 2.0, calc.operators['GANGE'], 3.0, ')']
        txt2 = "EXP(1.0PLUSS2.0GANGE3.0)"
        self.assertEqual(ex2, calc.parse_text(txt2))

    def test_complete_system(self):
        calc = calculator.Calculator()
        ex1 = "(3 MINUS 5) GANGE 5"
        ex2 = "EXP(12.2 PLUSS 3 GANGE 1)"
        ex3 = "SQRT(6 GANGE 6)"
        self.assertEqual(-10, calc.calculate_expression(ex1))
        self.assertAlmostEqual(3992786.8352109445, calc.calculate_expression(ex2))
        self.assertEqual(6, calc.calculate_expression(ex3))

if __name__ == '__main__':
    unittest.main()