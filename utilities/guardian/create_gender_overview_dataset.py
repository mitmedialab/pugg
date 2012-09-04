from name_gender import *
from sys import *
from glob import glob
import re
import csv
import os.path
import couchdb

genderer = NameGender("data/names/female_names_EN_GB.csv", "data/names/male_names_EN_GB.csv", "data/names/female_auxilliary_EN_GB.csv", "data/names/male_auxilliary_EN_GB.csv")

server = couchdb.Server()
paper = argv[1] 
db = server[paper]
##### USAGE ######
#output_file = argv[1] 
#output = csv.writer(open(output_file, "wb"))
#output.writerow(["year","month","yearweek","byline","gender",
#                 "articles","facebook","googleplus","twitter"])

return_data = {paper:{}}

emptybylines = 0
article_total = 0

def get_sharedata( gender, article, return_data):

  total = 0
  twitter = 0
  shares = 0
  likes = 0
  gplus = 0

  if "sharedata" in article and article["sharedata"]!=None:
#    try:
    if "googlePlus" in article["sharedata"]:
      gplus = article["sharedata"]["googlePlus"]["count"]
      if gplus == None:
        gplus = 0
      total += gplus
    if "twitter" in article["sharedata"]:
      twitter = article["sharedata"]["twitter"]["count"]
      if twitter == None:
        twitter = 0
      total += twitter
    if "facebook" in article["sharedata"]:
      if "shares" in article["sharedata"]["facebook"]:
        shares = article["sharedata"]["facebook"]["shares"]
        if shares == None:
          shares = 0
        total += shares
      if "likes" in article["sharedata"]["facebook"]:
        likes = article["sharedata"]["facebook"]["likes"]
        if likes == None:
          likes = 0
        total += likes

    if gender == None:
      return_data["facebook"] += shares + likes
      return_data["twitter"] += twitter
      return_data["googleplus"] += gplus
      return_data["social"] += shares + likes + twitter + gplus
    else:
      facebook_key = gender + "_facebook"
      twitter_key = gender + "_twitter"
      googleplus_key = gender  + "_googleplus"
      social_key = gender  + "_social"

      return_data[facebook_key] += shares + likes
      return_data[twitter_key] += twitter
      return_data[googleplus_key] += gplus
      return_data[social_key] += shares + likes + twitter + gplus
#    except Exception:
#      print "exception with social storage"
#      #omitted += 1
  return return_data


##### START THE SCRIPT ######
for row in db.view('_design/bylines/_view/bylinereport'): #, limit = 10000):
  article_total += 1
  article = row["value"]

#  if(paper == "dailymail" and "pubdate" in article and len(article["pubdate"])==8):
#    pubdate = article["pubdate"]
#    if(int(pubdate[0:4]) == 2011 and int(pubdate[4:6]) <= 6):
#      stdout.write('.')
#      continue

  if (not "sectionId" in article) or article["sectionId"] =="":
    print "x"
    section = "none"
  else:
    section = article["sectionId"]
  if( not (section in return_data[paper])):
    return_data[paper][section] = {"articles":0,"male":0,"female":0,"unknown":0,"social":0,"facebook":0,"twitter":0,"googleplus":0, "M_social":0, "F_social":0, "X_social":0, "M_facebook":0, "F_facebook":0, "X_facebook":0, "M_twitter":0, "F_twitter":0, "X_twitter":0, "M_googleplus":0, "F_googleplus":0, "X_googleplus":0, "emptybylines":0}
  
  return_data[paper][section]["articles"] += 1

  #add the generic share data
  if "sharedata" in article and article["sharedata"]!=None:
    return_data[paper][section] = get_sharedata(None, article, return_data[paper][section])

  if not ("bylines" in article):
    return_data[paper][section]["emptybylines"] += 1
    emptybylines += 1
    continue #fix this. should be reported as unknown
  for byline in article["bylines"]:

      byline = byline.lower().strip()

      if( re.search("press",byline) or re.search("reuters", byline) or 
        re.search("agencies", byline) or re.search("associated press",byline) or 
        byline =="ap" or byline =="" or
        (re.search("editor", byline) and len(byline.split(" ")) <=3) or 
        (re.search("correspondent", byline) and len(byline.split(" ")) <=3 ) or
        re.search("staff", byline) or len(byline) == 0):

        return_data[paper][section]["unknown"] += 1

      else:
        gender = genderer.estimate_gender(byline)
        if(gender == None):
          return_data[paper][section]["unknown"] += 1
          gender ="X"
        elif(gender =="M"):
          return_data[paper][section]["male"] += 1
        elif(gender == "F"):
          return_data[paper][section]["female"] += 1

  if "sharedata" in article and article["sharedata"]!=None:
#    try:
    return_data[paper][section] = get_sharedata(gender, article, return_data[paper][section])
#      total = 0
#      gplus = 0
#      twitter = 0
#      shares = 0
#      likes = 0
#      if "googlePlus" in article["sharedata"]:
#        gplus = article["sharedata"]["googlePlus"]["count"]
#        if gplus == None:
#          gplus = 0
#        return_data[paper][section]["googleplus"] += gplus
#        total += gplus
#      if "twitter" in article["sharedata"]:
#        twitter = article["sharedata"]["twitter"]["count"]
#        if twitter == None:
#          twitter = 0
#        return_data[paper][section]["twitter"] += twitter
#        total += twitter
#      if "facebook" in article["sharedata"]:
#        if "shares" in article["sharedata"]["facebook"]:
#          shares = article["sharedata"]["facebook"]["shares"]
#          if shares == None:
#            shares = 0
#          return_data[paper][section]["facebook"] += shares
#          total += shares
#        if "likes" in article["sharedata"]["facebook"]:
#          likes = article["sharedata"]["facebook"]["likes"]
#          if likes == None:
#            likes = 0
#          return_data[paper][section]["facebook"] += likes
#          total += likes
#      return_data[paper][section]["social"] = gplus + twitter + shares + likes

#    except Exception:
#      print "exception with social storage"
      #omitted += 1
 
output_file = argv[2] 
output = csv.writer(open(output_file, "wb"))

output.writerow(["paper","section","articles","male","female","unknown", "social", "facebook", "twitter", "googleplus", "M_social", "F_social", "X_social", "M_facebook", "F_facebook", "X_facebook", "M_twitter", "F_twitter", "X_twitter", "M_googleplus", "F_googleplus", "X_googleplus", "emptybylines"])

for section_name in return_data[paper]:
  section = return_data[paper][section_name]
  output.writerow([paper, section_name, section["articles"], section["male"], section["female"], section["unknown"], section["social"], section['facebook'], section['twitter'], section['googleplus'], section["M_social"], section["F_social"], section["X_social"], section["M_facebook"], section["F_facebook"], section["X_facebook"], section["M_twitter"], section["F_twitter"], section["X_twitter"], section["M_googleplus"], section["F_googleplus"], section["X_googleplus"], section['emptybylines']])


print "Total: " + str(article_total)
print "Empty Bylines: " + str(emptybylines)
