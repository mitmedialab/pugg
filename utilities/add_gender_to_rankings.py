from name_gender import *
from sys import *
from glob import glob
import re
import csv
import os.path

genderer = NameGender("data/names/female_names_EN_GB.csv", "data/names/male_names_EN_GB.csv", "data/names/female_auxilliary_EN_GB.csv", "data/names/male_auxilliary_EN_GB.csv")


##### USAGE ######
#python utilities/add_gender_to_rankings.py results/guardian/guardian/weekly_rankings/ results/guardian/guardian/weekly_gender_rankings/

for filename in glob(argv[1]+"*"):
  row_count = 0
  output_file = argv[2] + os.path.basename(filename) + ".gender.csv"
  output = csv.writer(open(output_file, "wb"))
  output.writerow(["year","month","yearweek","byline","gender",
                   "articles","facebook","googleplus","twitter"])

  with open(filename, 'rb') as f:
    print filename
    reader = csv.reader(f)
    for row in reader:
      if row_count == 0:
        row_count +=1
        continue

      row_count += 1
      return_row = []
      return_row.append(row[0]) #year
      return_row.append(row[1]) #month
      return_row.append(row[2]) #yearweek
      return_row.append(row[3]) #byline
      byline = row[3].lower().strip()
      if( re.search("press",byline) or re.search("reuters", byline) or 
        re.search("agencies", byline) or re.search("associated press",byline) or 
        byline =="ap" or byline =="" or
        (re.search("editor", byline) and len(byline.split(" ")) <=3) or 
        (re.search("correspondent", byline) and len(byline.split(" ")) <=3 ) or
        re.search("staff", byline) or len(byline) == 0):
        gender ="X"
      else:
        gender = genderer.estimate_gender(byline)
        if(gender == None):
          gender = "N"
      return_row.append(gender) #gender
      return_row.append(row[4]) #articles
      return_row.append(row[5]) #facebook
      return_row.append(row[6]) #googleplus
      return_row.append(row[7]) #twitter

      output.writerow(return_row)
