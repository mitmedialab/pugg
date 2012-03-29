from article import *
from article_accessor import *
from nytimes_article import *
from nytimes_article_accessor import *
import time

class ArticleAccessorBenchmarkController:
  def __init__(self):
    self.timeFilesystem()
    self.timeRedis()
    

  def timeFilesystem(self):
    print "Beginning Filesystem"
    print time.clock()
    articles = NYTimesArticleAccessor("data/nytimes")
    article_row = articles.getNextArticle()
    count = 0
    while article_row:
      try:
        article = articles.createArticle(article_row)
      except ValueError:
        article_row = articles.getNextArticle()
        continue
      count += 1
      article_row = articles.getNextArticle()
    print time.clock()
    print str(count) + " articles"
    print "Filesystem COMPLETE"

 
  def timeRedis(self):
    print "Beginning Redis"
    print time.clock()
    articles = ArticleAccessor()
    article = articles.getNextRedisArticle()
    count = 0
    while article:
      count+=1
      article = articles.getNextRedisArticle()
    print time.clock()
    print str(count) + " articles"
    print "Redis COMPLETE"

if __name__ == "__main__":
  benchmark_controller = ArticleAccessorBenchmarkController()
