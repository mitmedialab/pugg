from nytimes_article_accessor import *
from string import *
import os

def copy_fulltext_to_new_location(article):
  text_filename = article.filename.replace("data/full/", "data/nytimes-fulltext/").replace("xml", "txt")
  new_filename = article.filename.replace("data/full/", "test/fixtures/nytimes-data/").replace("xml", "txt")
  new_dir = os.path.dirname(new_filename)
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)
  os.system("cp " + text_filename + " " + new_filename)

article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
article = article_accessor.createArticle(article_accessor.getNextArticle())
copy_fulltext_to_new_location(article)
while(article):
  try:
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    copy_fulltext_to_new_location(article)
  except ValueError:
    continue
  except TypeError:
    break
