from time import time
from mongo_connection import *
from nytimes_article_accessor import *

class BenchmarkFilesMongoDB:
  def __init__(self):
    print "Benchmarking 50000 MongoDB records"
    current = time()
    self.benchmarkMongoDB()
    second_duration = time() - current
    print "Record Duration: " + str(second_duration)

    print "Benchmarking 50000 files"
    current = time()
    self.benchmarkFiles()
    first_duration = time() - current
    print "File Duration: " + str(first_duration)

  def benchmarkFiles(self, limit = 50000):
    self.articles = NYTimesArticleAccessor("data/nytimes")
    article_row = self.articles.getNextArticle()
    count =0 
    while article_row and count < limit:
      try:
        article = self.articles.createArticle(article_row)
      except ValueError:
        article_row = self.articles.getNextArticle()
        continue
      count += 1
      article_row = self.articles.getNextArticle()

  def benchmarkMongoDB(self, limit = 50000):
    self.db = MONGO_DB
    count = 0 
    for article in self.db.articles.find():
      if count >= limit:
        break
      count += 1
if __name__ == "__main__":
  benchmark = BenchmarkFilesMongoDB()

