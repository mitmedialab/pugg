from time import time
from mongo_connection import *
from nytimes_article_accessor import *
import re

class TaxonomicClassifierReport:
  def __init__(self):
    self.generate_report();

  def generate_report(self, limit = 5000000000):

    taxonomic_classifiers = {}

    self.articles = NYTimesArticleAccessor("data/nytimes")
    article_row = self.articles.getNextArticle()
    count =0 
    while article_row and count < limit:
      try:
        article = self.articles.createArticle(article_row)
      except ValueError:
        article_row = self.articles.getNextArticle()
        continue

      for classifier in article.taxonomic_classifiers:
        #if(re.search("/.*?/.*?/.*?/", classifier)):
        #  continue
        if classifier in taxonomic_classifiers:
          taxonomic_classifiers[classifier] += 1
        else:
          taxonomic_classifiers[classifier] = 0
      count += 1
      article_row = self.articles.getNextArticle()
    sorted_keys = sorted(taxonomic_classifiers, key=lambda key: taxonomic_classifiers[key])
    for key in sorted_keys:
      print re.sub(",", ".", str(taxonomic_classifiers[key])) + "," + key + ""

if __name__ == "__main__":
  benchmark = TaxonomicClassifierReport()

