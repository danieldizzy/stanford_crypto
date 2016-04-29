#!bin/python

# A small demo of doing unit testing in python.
# Tests ensure that your functions are doing what you expect them to do.
#
# To run it:
# $ python unittest_example.py            # Runs the actual 'assignment'
# $ python -m unittest unittest_example   # runs the tests


# This import is required for testing
import unittest

# The functions
def my_function(x, y):
    if x == 0:
        return y
    if x == 1:
        return y * 2
    return x * y

def main():
    # Use all the functions defined earlier.
    print my_function(55, 11)

if __name__ == '__main__':
    main()    


# ------------------------------------------
# Tests exercise the functions

# class must inherit from unittest.TestCase:
class Tests(unittest.TestCase):

    # function name must begin with 'test':
    def test_my_function(self):
        # This is just one possible way of writing tests.
        # Do whatever works for you.
        
        # Try changing some of the data here,
        # and see what happens when you run the tests.
        test_cases = [
            [1, 2, 4],
            [0, 2, 2],
            [3, 4, 12]
        ]
        for (x, y, expected_output) in test_cases:
            # self.assertEqual is a Python unittest method.
            # there are other assertions available, you can google them.
            self.assertEqual(expected_output, my_function(x, y))
