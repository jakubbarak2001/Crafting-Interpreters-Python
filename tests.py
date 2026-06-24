import unittest
from main import scan_operators


class TestArithmeticOperatorsScanning(unittest.TestCase):
    expected_output = ["OP (+)", "OP (-)", "OP (*)", "OP (/)"]
    def test_standard_operators(self):
        incoming_data = ["+", "-", "*", "/"]
        self.assertEqual(scan_operators(incoming_data), self.expected_output)

    def test_operators_with_whitespace(self):
        incoming_data_whitespace = ["  +", "-   ", "   *    ", "/"]
        self.assertEqual(scan_operators(incoming_data_whitespace), self.expected_output)

if __name__ == '__main__':
    unittest.main()

