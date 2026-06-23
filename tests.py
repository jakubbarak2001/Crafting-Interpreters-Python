import unittest

class TestArithmeticOperatorsScanning(unittest.TestCase):
    def test_plus(self):
        self.assertEqual("1+1", "OP (+)")

if __name__ == '__main__':
    unittest.main()
