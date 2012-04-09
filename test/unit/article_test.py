import unittest
import test_common

class ArticleTest(unittest.TestCase):
  def runTest(self):
    assert 0

test_common.ALL_TESTS.append(ArticleTest)

if __name__ == '__main__':
  unittest.main()
