import os
import sys
import unittest
from unittest import TestLoader, TextTestRunner


class NumbersTestResult(unittest.TextTestResult):
    def addSubTest(self, test, subtest, outcome):
        super(NumbersTestResult, self).addSubTest(test, subtest, outcome)
        self.testsRun += 1


loader = TestLoader()
suite = loader.discover("tests")

os.environ["ENVIRONMENT"] = "TEST"

runner = TextTestRunner(verbosity=2, resultclass=NumbersTestResult)
result = runner.run(suite)
sys.exit(not result.wasSuccessful())
