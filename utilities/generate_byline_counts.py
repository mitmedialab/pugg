from nytimes_article_accessor import *
from article import *
from name_gender import *

articles = NYTimesArticleAccessor("data/nytimes")
genderer = NameGender("data/names/female_names.csv", "data/names/male_names.csv")

article = articles.createArticle(articles.getNextDBArticle())
no_bylines = 0
bylines = 0
male = 0
female = 0
none = 0

while article:
  if(len(article.byline.strip()) == 0):
    no_bylines += 1
  else:
    bylines += 1
    gender = genderer.estimate_gender(article.byline)
    if(gender == "M"):
      male += 1
    elif(gender == "F"):
      female += 1
    else:
      none += 1
  try:
  article = articles.createArticle(articles.getNextArticle())
  count += 1
  except ValueError:
    article = articles.createArticle(articles.getNextArticle())



print "bylines: " + str(bylines)
print "no bylines: " + str(no_bylines)
print "female: " + str(female)
print "male: " + str(male)
print "none:" + str(none)
