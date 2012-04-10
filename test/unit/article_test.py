import unittest
import test_common
from article import *
from nytimes_article_accessor import *

class ArticleTest(unittest.TestCase):
  def setUp(self):
    test_common.MONGO_DB.articles.remove()
    self.assertEqual(0, test_common.MONGO_DB.articles.count())

  def tearDown(self):
    MONGO_DB.articles.remove()
    self.assertEqual(0, test_common.MONGO_DB.articles.count())
    
  def testSave(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    self.assertEqual(0, MONGO_DB.articles.count())
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    article.save()
    self.assertEqual(1, MONGO_DB.articles.count())
    self.assertEqual(article.headline, MONGO_DB.articles.find_one()["headline"])

  #def testGetDataFileObject():

test_common.ALL_TESTS.append(ArticleTest)

if __name__ == '__main__':
  unittest.main()
