import unittest
from nytimes_article_accessor import *

class NYTimesArticleAccessorTest(unittest.TestCase):
  def setUp(self):
    self.article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
  def testGetNextMonth(self):
    month = self.article_accessor.getNextMonth()
    self.assertEqual(20, len(month))
    month = self.article_accessor.getNextMonth()
    self.assertEqual(19, len(month))
    month = self.article_accessor.getNextMonth()
    self.assertEqual(None, month)

if __name__ == '__main__':
  unittest.main()
