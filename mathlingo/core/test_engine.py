import unittest
from engine import MathEngine

class TestMathEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MathEngine()

    def test_valid_numeric_answers(self):
        self.assertTrue(self.engine.check_answer("27", "27"))
        self.assertTrue(self.engine.check_answer("10.5", "10.5"))
        self.assertTrue(self.engine.check_answer(" -5 ", "-5"))

    def test_invalid_input_formats(self):
        self.assertFalse(self.engine.check_answer("twenty-seven", "27"))
        self.assertFalse(self.engine.check_answer("27; DROP TABLE users;", "27"))
        self.assertFalse(self.engine.check_answer("", "0"))

if __name__ == "__main__":
    unittest.main()