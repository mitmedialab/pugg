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

  def assertInitDict(self, article_dict):
    article = Article(article_dict)
    self.assertTrue(article.source != None)
    self.assertTrue(article.headline != None)
    self.assertTrue(article.byline != None)
    self.assertTrue(article.fulltext != None)
    self.assertTrue(article.pub_date != None)
    return article

  #This test needs to be improved
  def testInit(self):
    #we set up and teardown the fixtures to grab a single hash
    test_common.CommonSetup.setupNYTimesFixtures()
    article_dict = MONGO_DB.articles.find_one()
    test_common.CommonSetup.teardownNYTimesFixtures()

    article_dict.pop("article_type")
    article = self.assertInitDict(article_dict)
    self.assertEqual("Article", article.article_type)

    article_dict["article_type"] = "NYTimesArticle"
    try:
      article = self.assertInitDict(article_dict)
    except Exception as e:
      self.assertEqual(NameError, type(e))
    
  def testSave(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    self.assertEqual(0, MONGO_DB.articles.count())
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    article.save()
    self.assertEqual(1, MONGO_DB.articles.count())
    self.assertEqual(article.headline, MONGO_DB.articles.find_one()["headline"])

  def testGetDataFileObject(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    self.assertEqual("charles isherwood", article.byline)
    fulltext = open("test/fixtures/nytimes-data/2007/06/01/1851199.txt").read()
    article.fulltext = article.getDataFileObject("data/full/", "test/fixtures/nytimes-data/", "txt").read()
    self.assertEqual(fulltext,article.fulltext)

    #skip dud row
    article_accessor.getNextArticle()
    #now check the next row
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    fulltext = open("test/fixtures/nytimes-data/2007/06/01/1851247.txt").read()
    article.fulltext = article.getDataFileObject("data/full/", "test/fixtures/nytimes-data/", "txt").read()
    self.assertEqual(fulltext,article.fulltext)
   

test_common.ALL_TESTS.append(ArticleTest)

if __name__ == '__main__':
  unittest.main()
