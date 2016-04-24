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

    def test_poly_to_bin_2(self):
        x = (7,6,0)
        self.assertEqual(0xc1, aes.poly_to_bin(x))

    def test_bin_to_poly(self):
        x = 0b101101
        self.assertEqual([5, 3, 2, 0], aes.bin_to_poly(x))

    def test_add_binary_poly(self):
        # powers of 2, sec 4.1
        x1 = (6,4,2,1,0)
        x2 = (7,1,0)
        self.assertEqual([7,6,4,2], aes.add_binary_poly(x1, x2))

    def test__multiply_poly(self):
        # Top of page 11
        a = (6, 4, 2, 1, 0)
        b = (7, 1, 0)
        expected = [13, 11, 9, 8, 6, 5, 4, 3, 0]
        self.assertEqual(expected, aes._multiply_poly(a, b))

    def test_poly_from_string(self):
        self.assertEqual(aes.poly_from_string('x^7 + x^5 + x^2 + x^0'), [7,5,2,0])
        self.assertEqual(aes.poly_from_string('x^7+x^5+x^2+x^0'), [7,5,2,0])
        self.assertEqual(aes.poly_from_string('x+1'), [1,0])
        
    def test_poly_divmod(self):
        
        data = (
            ('1', 'x^1', '', '1'),
            ('x', 'x', '1', ''),
            ('x^3 + x', 'x', 'x^2 + 1', ''),
            # Example from page 11:
            ('x^13 + x^11 + x^9 + x^8 + x^6 + x^5 + x^4 + x^3 + 1',
             'x^8 + x^4 + x^3 + x + 1',
             'x^5 + x^3',
             'x^7 + x^6 + 1'),
        )
        for (n, d, exp_q, exp_r) in data:
            n, d, exp_q, exp_r = map(aes.poly_from_string, (n, d, exp_q, exp_r))
            actual_q, actual_rem = aes.poly_divmod(n, d)
            self.assertEqual(exp_q, actual_q)
            self.assertEqual(exp_r, actual_rem)

    def test_bigdot_multiply_polys(self):
        # sec 4.2 Multiplication
        a = 0x57
        b = 0x83
        actual = aes.bigdot_multiply(a, b)
        expected = aes.bin_to_poly(0xc1)
        self.assertEqual(expected, actual)

    def test_get_subbytes_single_result(self):
        # page 16
        s = 0x53
        self.assertEqual(0xed, aes.get_subbytes_transformation(s))

    def test_do_state_subbytes_transformation(self):
        state = aes.load_state(range(0, 16))
        self.assertEqual(0, state[0][0])
        self.assertEqual(4, state[0][1])
        transformed = aes.subbyte_transform_state(state)
        self.assertEqual(transformed[0][0], 0x63)
        self.assertEqual(transformed[0][1], 0xf2)

