import unittest
from app import app, db
from app.utils import custom_function

class TestUtils(unittest.TestCase):

    def test_custom_function(self):
        result = custom_function('test_input')
        self.assertEqual(result, 'test_output')

if __name__ == '__main__':
    unittest.main()