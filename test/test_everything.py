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

        # mult by x
        a = [8]
        b = [1]
        self.assertEqual([9], aes._multiply_poly(a, b))

    def test_poly_from_string(self):
        self.assertEqual(aes.poly_from_string('x^7 + x^5 + x^2 + x^0'), [7,5,2,0])
        self.assertEqual(aes.poly_from_string('x^7+x^5+x^2+x^0'), [7,5,2,0])
        self.assertEqual(aes.poly_from_string('x+1'), [1,0])

    def test_poly_divmod(self):
        data = (
            ('1', '1', '1', ''),
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
        actual = aes.bigdot_multiply(0x57, 0x83)
        expected = aes.bin_to_poly(0xc1)
        self.assertEqual(expected, actual)

        # pg 12
        actual = aes.bigdot_multiply(0x57, 0x13)
        expected = aes.bin_to_poly(0xfe)
        self.assertEqual(expected, actual)

        # poly multiply by x results in a shift and the top bit is
        # chopped off due to modulo m(x) (which is 'x^8+x^4+x^3+x+1')
        actual = aes.bigdot_multiply(0x80, 0x02)
        expected = [4, 3, 1, 0]
        self.assertEqual(expected, actual)


    def test_xtime(self):
        # page 12
        self.assertEqual(aes.xtime(0x57), 0xae)
        self.assertEqual(aes.xtime(0xae), 0x47)
        self.assertEqual(aes.xtime(0x47), 0x8e)
        self.assertEqual(aes.xtime(0x8e), 0x07)

        # Note the top bit has been chopped off here:
        self.assertEqual(aes.xtime(0x80), 0b00011011)
        # 0x80 = 0b 1000 0000.  Multiply by x

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

    def test_shiftrows(self):
        i = range(0, 16)
        state = aes.load_state(i)  # creates [[0,4,8,12],[1,5, ...], ...]
        actual = aes.shift_rows(state)
        expected = [
            [0,4,8,12],
            [5,9,13,1],
            [10,14,2,6],
            [15,3,7,11]
        ]
        self.assertEqual(actual, expected)

    def test_mix_single_column(self):
        # c = [1,1,1,1]
        # actual = aes.mix_single_column(c)
        # self.assertEqual([1,1,1,1], actual)

        test_cases = [
            # Test vectors from
            # https://en.wikipedia.org/wiki/Rijndael_mix_columns:
            [[219, 19, 83, 69], [142, 77, 161, 188]],
            [[242, 10, 34, 92], [159, 220, 88, 157]],
            [[1, 1, 1, 1], [1, 1, 1, 1]],
            [[198, 198, 198, 198], [198, 198, 198, 198]],
            [[212, 212, 212, 213], [213, 213, 215, 214]],
            [[45, 38, 49, 76], [77, 126, 189, 248]],

            # from www.angelfire.com/biz7/atleast/mix_columns.pdf:
            # [[0xd4, 0xbf, 0x5d, 0x30], [0x04, 0x66, 0x81, 0xe5]]
        ]

        for t, expected_output in test_cases:
            actual = aes.mix_single_column(t)
            self.assertEqual(expected_output, actual)

    def test_GF_256_byte_multi_should_equal_bigdot_multiply(self):
        for i in [219, 242, 1, 198, 212, 45]:
            for j in [2, 3]:
                g = aes.GF_256_byte_mult(j, i)
                b = aes.poly_to_bin(aes.bigdot_multiply(j, i))
                self.assertEqual(g, b)
