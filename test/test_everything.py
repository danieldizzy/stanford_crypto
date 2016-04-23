# Sanity checks only to ensure everything runs, not real tests.
#
# If you're learning how to code, don't do things this way.

import unittest
from cStringIO import StringIO
import sys
import os

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
