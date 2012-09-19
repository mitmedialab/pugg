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
ag_key = {"X":"unknown", "M":"male", "F":"female", "B": "mixed"}

emptybylines = 0
article_total = 0

def get_sharedata(article):
  return_data["social"] = 0
  return_data["facebook"] = 0
  return_data["twitter"] = 0
  return_data["googleplus"] = 0

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
    if "twitter" in article["sharedata"] and "count" in article["sharedata"]["twitter"]:
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

    return_data["facebook"] += shares + likes
    return_data["twitter"] += twitter
    return_data["googleplus"] += gplus
    return_data["social"] += shares + likes + twitter + gplus
  return return_data


##### START THE SCRIPT ######

output_file = argv[2]
output = csv.writer(open(output_file, "wb"))

output.writerow(["paper","section", "title", "gender", "date", "bylines", "social", "facebook", "twitter", "googleplus", "url"])


for row in db.view('_design/bylines/_view/bylinereport'):
  article = row["value"]
  article_gender = "X"

  if((paper =="telegraph" or paper == "dailymail" )and "pubdate" in article and len(article["pubdate"])==8):
    pubdate = article["pubdate"]

  if(paper =="guardian" and "webPublicationDate" in article):
    pubdate = article["webPublicationDate"]
    date = pubdate.split("-")
    if( ( int(date[0]) == 2011 and int(date[1]) <= 6) or
        ( int(date[0]) == 2012 and int(date[1]) >=7)):
      stdout.write('.')
      emptybylines += 1
      continue
  
  if(paper == "dailymail"):
    if(int(pubdate[0:4]) == 2011 and int(pubdate[4:6]) <= 6):
      stdout.write('.')
      continue

  if(paper == "telegraph" and "pubdate" in article and len(article["pubdate"])>0):
    date = article["pubdate"].split("-")
    pubmonth = article["pubdate"][0:7]
    if( ( int(date[0]) == 2011 and int(date[1]) <= 6) or
        ( int(date[0]) == 2012 and int(date[1]) >=7)):
      stdout.write('.')
      emptybylines += 1
      continue

  if(paper=="telegraph" and(("fulltext" in article and len(article["fulltext"].strip()) ==0) or not ("fulltext" in article))):
    stdout.write('x')
    emptybylines += 1
    continue

  if(paper == "dailymail" and "pubdate" in article):
    pubmonth = article["pubdate"][0:4] + "-" + article["pubdate"][4:6]
  elif(paper == "guardian" and "webPublicationDate" in article):
    pubmonth = article["webPublicationDate"][0:7]

  if (not "sectionId" in article) or article["sectionId"] =="":
    print "x"
    section = "none"
  else:
    section = article["sectionId"]

  #possible article_gender values:
  # X: unknown
  # M: all male
  # F: all female
  # B: Mixed

  bylines =""

  if not ("bylines" in article):
    emptybylines += 1
    article_gender = "E"
  else:
    for byline in article["bylines"]:

      byline = re.sub('<[^<]*?/?>', "", byline)
      byline = re.sub("\n", "", byline)
      byline = byline.lower().strip()
      if byline == "":
        continue

      if(bylines==""):
        bylines += byline
      else:
        bylines += "|" + byline

      if( re.search("press",byline) or re.search("reuters", byline) or 
        re.search("agencies", byline) or re.search("associated press",byline) or 
        byline =="ap" or byline =="" or
        (re.search("editor", byline) and len(byline.split(" ")) <=3) or 
        (re.search("correspondent", byline) and len(byline.split(" ")) <=3 ) or
        re.search("staff", byline) or len(byline) == 0):

        gender ="X" #we're calling all unknown ones "X"

      else:
        gender = genderer.estimate_gender(byline)
        if(gender == None):
          gender ="X"

      #decide article gender 
      if(article_gender=="X" and gender !="X"):
        article_gender = gender
      elif (article_gender!="B" and article_gender != gender):
        article_gender = "B"
  sharedata = get_sharedata(article)

  title = ""
  if("title" in article):
    title = article["title"]

  url = ""
  if("url" in article):
    url = article["url"]

  output.writerow([paper, section, title, article_gender, pubdate, bylines.encode("ascii", 'xmlcharrefreplace'), sharedata["social"],sharedata["facebook"], sharedata["twitter"], sharedata["googleplus"], url])




