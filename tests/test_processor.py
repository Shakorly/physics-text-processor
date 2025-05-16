import unittest
from physics_text_processor import RobustPhysicsTextProcessor

class TestProcessor(unittest.TestCase):
    def test_basic_cleaning(self):
        processor = RobustPhysicsTextProcessor()
        self.assertEqual(processor.process("  hello  "), "hello")

if __name__ == "__main__":
    unittest.main()