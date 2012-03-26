import unittest
from article import *
from nytimes_article import *
from nytimes_article_accessor import *

class ArticleAccessorTest(unittest.TestCase):
  def setUp(self):
    config.PUGG_DB=2
    self.article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    self.article = self.article_accessor.createArticle(self.article_accessor.getNextArticle())
    self.article.establishConnection()
    self.article.puggdb.flushdb()
    self.article.save()
    self.article = self.article_accessor.createArticle(self.article_accessor.getNextArticle())
    self.article.save()

  def tearDown(self):
    self.article.puggdb.flushdb()

  def testGetNextRedisArticle(self):
    next_article = self.article_accessor.getNextRedisArticle()
    self.assertEqual("2 More Democratic Candidates Decline to Join in Fox News Debate", next_article.headline)
    next_article = self.article_accessor.getNextRedisArticle()
    self.assertEqual("'MY TRIP TO AL-QAEDA'", next_article.headline)
    next_article = self.article_accessor.getNextRedisArticle()
    self.assertEqual(None, next_article)

if __name__ == '__main__':
  unittest.main()
