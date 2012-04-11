import unittest
import test_common
from mediacloud_article import *

class MediaCloudArticleTest(unittest.TestCase):
  def setUp(self):
    test_common.CommonSetup.setupMediaCloudFixtures()

  def tearDown(self):
    test_common.CommonSetup.teardownMediaCloudFixtures()
    test_common.MONGO_DB.mediacloud_articles.remove()

  def assertInitDict(self, article_dict):
    article = MediaCloudArticle(article_dict)
    self.assertTrue(article.source != None)
    self.assertTrue(article.headline != None)
    self.assertTrue(article.byline != None)
    self.assertTrue(article.fulltext != None)
    self.assertTrue(article.pub_date != None)
    return article
    
  def testSave(self):
    articles = test_common.MONGO_DB.mc_import_articles.find()

    article_dict = articles[0]
    article = self.assertInitDict(article_dict)
    print article_dict
    self.assertEqual("MediaCloudArticle", article.article_type)


test_common.ALL_TESTS.append(MediaCloudArticleTest)

if __name__ == '__main__':
  unittest.main()
