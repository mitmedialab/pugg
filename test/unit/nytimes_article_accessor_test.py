import unittest
import test_common
from nytimes_article_accessor import *
from string import *
import datetime

import config
config.PUGG_DB="pugg_test"


class NYTimesArticleAccessorTest(unittest.TestCase):
  def setUp(self):
    self.article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    test_common.CommonSetup.setupNYTimesFixtures()

  def tearDown(self):
    test_common.CommonSetup.teardownNYTimesFixtures()


  def testGetNextMonth(self):
    month = self.article_accessor.getNextMonth()
    self.assertEqual(21, len(month))
    month = self.article_accessor.getNextMonth()
    self.assertEqual(19, len(month))
    month = self.article_accessor.getNextMonth()
    self.assertEqual(None, month)

  def testGetNextArticle(self):
    for i in range(40):
      assert self.article_accessor.getNextArticle() != None, 'iterating through next articles, ' + str(i) + ' returned None'
    self.assertEqual(None, self.article_accessor.getNextArticle())

  def testGetNextDBArticle(self):
    #this one counts to 39, since there are actually 39 articles
    #but the csv testGetNextArticle method is a stage before the CSV is
    # striped of its extraneous header line. There is no dummy record in Mongo
    for i in range(39):
      assert self.article_accessor.getNextDBArticle() != None, 'iterating through next articles, ' + str(i) + ' returned None'
    self.assertEqual(None, self.article_accessor.getNextDBArticle())

  def testCreateArticle(self):
    article = self.article_accessor.createArticle(self.article_accessor.getNextArticle())
    self.assertEqual("'MY TRIP TO AL-QAEDA'", article.headline)
    self.assertEqual("charles isherwood", article.byline)
    self.assertEqual(['Top', 'Top/Features', 
      'Top/Features/Arts', 'Top/Features/Movies', 'Top/News'], 
      article.taxonomic_classifiers)

test_common.ALL_TESTS.append(NYTimesArticleAccessorTest)

if __name__ == '__main__':
  unittest.main()
