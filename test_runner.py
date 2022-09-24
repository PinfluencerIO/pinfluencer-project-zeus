import os
import shutil
import sys
import unittest
from unittest import TestLoader, TextTestRunner


# to count subtests in test count
class NumbersTestResult(unittest.TextTestResult):
    def addSubTest(self, test, subtest, outcome):
        super(NumbersTestResult, self).addSubTest(test, subtest, outcome)
        self.testsRun += 1


loader = TestLoader()
suite = loader.discover("tests")

# for logging and other DI switching
os.environ["ENVIRONMENT"] = "TEST"

# copy template for sanity check tests
try:
    template_yaml_file = "template.yaml"
    shutil.copy(template_yaml_file, f"tests/{template_yaml_file}")
except FileNotFoundError:
    ...

# run tests
runner = TextTestRunner(verbosity=2, resultclass=NumbersTestResult)
result = runner.run(suite)

# remove copied template for unit tests
try:
    os.remove(f"tests/{template_yaml_file}")
except FileNotFoundError:
    ...
sys.exit(not result.wasSuccessful())
