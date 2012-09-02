from name_gender import *
from sys import *
from glob import glob
import re
import csv
import os.path
import couchdb

genderer = NameGender("data/names/female_names_EN_GB.csv", "data/names/male_names_EN_GB.csv", "data/names/female_auxilliary_EN_GB.csv", "data/names/male_auxilliary_EN_GB.csv")

server = couchdb.Server()
db = server["guardian"]
##### USAGE ######
#output_file = argv[1] 
#output = csv.writer(open(output_file, "wb"))
#output.writerow(["year","month","yearweek","byline","gender",
#                 "articles","facebook","googleplus","twitter"])

paper = "telegraph"
return_data = {paper:{}}

for index in db.view('_all_docs'):
  article = db.get(index['id'])
  section = article["sectionId"]
  if( not (section in return_data[paper])):
    return_data[paper][section] = {"articles":0,"male":0,"female":0,"unknown":0,"social":0,"facebook":0,"twitter":0,"googleplus":0, "emptybylines":0}
  
  return_data[paper][section]["articles"] += 1
  if not ("bylines" in article):
    return_data[paper][section]["emptybylines"] += 1
    continue
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
        elif(gender =="M"):
          return_data[paper][section]["male"] += 1
        elif(gender == "F"):
          return_data[paper][section]["female"] += 1

  if "sharedata" in article and article["sharedata"]!=None:
    total = 0
    gplus = 0
    twitter = 0
    shares = 0
    likes = 0
    if "googlePlus" in article["sharedata"]:
      gplus = article["sharedata"]["googlePlus"]["count"]
      return_data[paper][section]["googleplus"] += gplus
      total += gplus
    if "twitter" in article["sharedata"]:
      twitter = article["sharedata"]["twitter"]["count"]
      return_data[paper][section]["twitter"] += twitter
      total += twitter
    if "facebook" in article["sharedata"]:
      if "shares" in article["sharedata"]["facebook"]:
        shares = article["sharedata"]["facebook"]["shares"]
        return_data[paper][section]["facebook"] += shares
        total += shares
      if "likes" in article["sharedata"]["facebook"]:
        likes = article["sharedata"]["facebook"]["likes"]
        return_data[paper][section]["facebook"] += likes
        total += likes
    return_data[paper][section]["social"] = gplus + twitter + shares + likes

output_file = argv[1] 
output = csv.writer(open(output_file, "wb"))
output.writerow(["paper","section","articles","male","female","unknown", "social", "facebook", "twitter", "googleplus", "emptybylines"])

for section_name in return_data[paper]:
  section = return_data[paper][section_name]
  output.writerow(paper, section_name, section["articles"], section["male"], section["female"], section["unknown"], section["social"], section['facebook'], section['twitter'], section['googleplus'], section['emptybylines'])
