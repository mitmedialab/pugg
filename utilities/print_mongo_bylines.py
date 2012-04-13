from nytimes_article_accessor import *
from article import *
from name_gender import *

genderer = NameGender("data/names/female_names.csv", "data/names/male_names.csv")

no_bylines = 0
bylines = 0
male = 0
female = 0
none = 0
none_bylines = {}

for article in MONGO_DB.articles.find({}, {'byline':1}):
  byline = article["byline"].strip()
  if(len(byline) == 0):
    no_bylines += 1
  else:
    bylines += 1
    gender = genderer.estimate_gender(byline)
    if(gender == "M"):
      male += 1
    elif(gender == "F"):
      female += 1
    else:
      none += 1
      if none_bylines.has_key(byline):
        none_bylines[byline] += 1
      else:
        none_bylines[byline] = 1

print "bylines: " + str(bylines)
print "no bylines: " + str(no_bylines)
print "female: " + str(female)
print "male: " + str(male)
print "none:" + str(none)

top_bylines = sorted(none_bylines, key=lambda key: none_bylines[key], reverse=True)
for i in range(100):
  if i >= len(top_bylines):
    break
  print str(none_bylines[top_bylines[i]]) + "," + top_bylines[i]
