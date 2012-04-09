import unittest
import sample_class
import test_common

class SampleClassTest(unittest.TestCase):
  def runTest(self):
    assert 1

test_common.ALL_TESTS.append(SampleClassTest)

if __name__ == '__main__':
  unittest.main()
