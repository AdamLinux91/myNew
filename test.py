import unittest
from script import sum
class SumTest(unittest.TestCase):

    def test_sum(self):
        result = sum(3, 5)
        self.assertEqual(result, 8)
    
    def test_str_handling(self):
        result = sum('x', 'y')
        self.assertEqual(result, "invalid inputs")
    
    def test_handl_inputs(self):
        result = sum('w', 5)
        self.assertEqual(result, "invalid inputs")

unittest.main()
