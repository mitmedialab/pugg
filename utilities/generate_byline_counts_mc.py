from nytimes_article_accessor import *
import mongo_connection
from article import *
from mediacloud_article import *
from name_gender import *

articles = MONGO_DB.mc_import_articles.find()
genderer = NameGender("data/names/female_names.csv", "data/names/male_names.csv", "data/names/female_auxilliary.csv", "data/names/male_auxilliary.csv")

no_bylines = 0
bylines = 0
male = 0
female = 0
none = 0

for article_dict in articles:
  article = MediaCloudArticle(article_dict)
  #import pdb;pdb.set_trace()
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

print "bylines: " + str(bylines)
print "no bylines: " + str(no_bylines)
print "female: " + str(female)
print "male: " + str(male)
print "none:" + str(none)
