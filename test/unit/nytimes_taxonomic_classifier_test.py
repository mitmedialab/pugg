import unittest
import test_common
from nytimes_article import *
from nytimes_article_accessor import *
from nytimes_taxonomic_classifier import *

class NYTimesTaxonomicClassifierTest(unittest.TestCase):
  def setUp(self):
    self.taxonomic_classifier = NYTimesTaxonomicClassifier("data/utility-data/nytimes_taxonomic_classifier_exclusion.yml", "data/utility-data/nytimes_taxonomic_classifier_aggregation.yml")

  def testCountPronounGender(self):
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    classifiers = self.taxonomic_classifier.winnow(article.taxonomic_classifiers)
    self.assertEqual(4, len(classifiers))

    article_accessor.getNextArticle() #skip second line
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    classifiers = self.taxonomic_classifier.winnow(article.taxonomic_classifiers)
    self.assertEqual(3, len(classifiers))

    article = article_accessor.createArticle(article_accessor.getNextArticle())
    classifiers = self.taxonomic_classifier.winnow(article.taxonomic_classifiers)
    self.assertTrue("Top/Classifieds" not in classifiers)
    self.assertTrue("Top/Classifieds/Job Market" not in classifiers)
    self.assertTrue("Top/News" in classifiers)
    self.assertTrue("Top/Features/Books" in classifiers)
    self.assertTrue("Top/News/New York and Region/Columns" not in classifiers)
    
    for i in range(9):
      article_accessor.getNextArticle()

    article = article_accessor.createArticle(article_accessor.getNextArticle())
    classifiers = self.taxonomic_classifier.winnow(article.taxonomic_classifiers)
    self.assertEqual(["Opinion"], classifiers)

      
test_common.ALL_TESTS.append(NYTimesTaxonomicClassifierTest)

if __name__ == '__main__':
  unittest.main()
