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

  def testGetNextArticle(self):
    for i in range(39):
      assert self.article_accessor.getNextArticle() != None, 'iterating through next articles, ' + str(i) + ' returned None'
    self.assertEqual(None, self.article_accessor.getNextArticle())

if __name__ == '__main__':
  unittest.main()
