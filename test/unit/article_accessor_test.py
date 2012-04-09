import unittest
import test_common
from article import *
from nytimes_article import *
from nytimes_article_accessor import *

class ArticleAccessorTest(unittest.TestCase):
  def setUp(self):
    return None

  def tearDown(self):
    return None

test_common.ALL_TESTS.append(ArticleAccessorTest)

if __name__ == '__main__':
  unittest.main()

