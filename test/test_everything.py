# Sanity checks only to ensure everything runs, not real tests.
#
# If you're learning how to code, don't do things this way.

import unittest
from cStringIO import StringIO
import sys
import os
import week_2.aes as aes

class TestBase(unittest.TestCase):

    def setUp(self):
        # Capture output during tests.
        self.iobuff = StringIO()
        sys.stderr = sys.stdout = self.iobuff

        # Hack to view output if needed
        self.printstdout = False

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        if self.printstdout:
            print self.iobuff.getvalue()

    def p(self):
        """Lazy shorthand to print results."""
        self.printstdout = True

class Helpers(TestBase):

    def test_helpers(self):
        import lib.helpers
        lib.helpers.main()

class Week_1(TestBase):

    def test_q1(self):
        import week_1.assignment.q7

    def test_bonus(self):
        import week_1.assignment.bonus

    def test_birthday_paradox_8_days(self):
        import week_1.misc.birthday_paradox_8_days

class Week_2(TestBase):

    def test_assignment(self):
        import week_2.assignment
        week_2.assignment.main()

    def test_bonus(self):
        import week_2.bonus
        week_2.bonus.main()


class Test_AES(unittest.TestCase):
    """Test cases lifted from http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
    where possible."""

    def test_load_state(self):
        i = range(0, 16)
        expected = [[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]]
        self.assertEqual(4, expected[0][1])
        self.assertEqual(expected, aes.load_state(i))

    def test_output_state(self):
        i = range(0, 16)
        o = aes.output_state(aes.load_state(i))
        self.assertEqual(i, o)

    def test_poly_to_bin(self):
        x1 = (5,3,2,0)
        self.assertEqual(0b101101, aes.poly_to_bin(x1))

    def test_bin_to_poly(self):
        x = 0b101101
        self.assertEqual([5, 3, 2, 0], aes.bin_to_poly(x))

    def test_add_binary_poly(self):
        # powers of 2, sec 4.1
        x1 = (6,4,2,1,0)
        x2 = (7,1,0)
        self.assertEqual([7,6,4,2], aes.add_binary_poly(x1, x2))

