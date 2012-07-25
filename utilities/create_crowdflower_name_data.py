from nytimes_article_accessor import *
from article import *
from name_gender import *
from nytimes_taxonomic_classifier import *
from re import *

articles = NYTimesArticleAccessor("data/nytimes-selection")
genderer = NameGender("data/names/female_names_EN_US.csv", "data/names/male_names_EN_US.csv", "data/names/female_auxilliary.csv", "data/names/male_auxilliary.csv")

article = articles.createArticle(articles.getNextArticle())
no_bylines = 0
bylines = 0
male = 0
female = 0
none = 0

names = []

while article:
  if len(names) >= 50:
    break

  if(len(article.byline.strip()) == 0):
    no_bylines += 1
  else:
    bylines += 1
    names.append(article.byline.strip())
    names = list(set(names))
  try:
    article = articles.createArticle(articles.getNextArticle())
  except ValueError:
    article = articles.createArticle(articles.getNextArticle())

for name in names:
  gender = genderer.estimate_gender(name)
  if(gender ==None):
    gender = "N"
  name = sub(r',',' ', name)
  name = sub(r';.*?$', "",name)
  namestring =  sub(r' ','+', name)
  print(name + "," + gender + ",https://www.google.com/search?site=imghp&tbm=isch&q=" + namestring +"+New+York+Times")
