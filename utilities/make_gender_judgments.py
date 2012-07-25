from name_gender import *
from sys import *
import re
import csv

genderer = NameGender("data/names/female_names_EN_US.csv", "data/names/male_names_EN_US.csv", "data/names/female_auxilliary.csv", "data/names/male_auxilliary.csv")

#output = csv.writer(open(argv[2], "wb"))
male = {}
female = {}
unknown = {}
unreported = {}

male_count = 0
female_count = 0
unknown_count = 0 
unreported_count = 0
total_articles = 0
total_bylines = 0

with open(argv[1], 'rb') as f:
  reader = csv.reader(f)
  for row in reader:
    return_row = []
    return_row.append(row[0])
    total_articles += 1

    splitrow = []
    if(len(row) == 1 or row[1].strip()==""):
      unreported_count += 1
    else:
      for i in range(len(row)-1):
        i = i+1
        names = row[i].split("and")
        splitrow.extend(names)
      for i in range(len(splitrow)):
        total_bylines += 1
        byline = splitrow[i].strip().lower()
        if( re.search("press",byline) or re.search("reuters", byline) or 
            re.search("agencies", byline) or re.search("associated press",byline) or 
            (re.search("editor", byline) and len(byline.split(" ")) <=3) or 
            (re.search("correspondent", byline) and len(byline.split(" ")) <=3 ) or
            re.search("staff", byline) or len(byline) == 0):
          unreported_count += 1
          gender ="X"
          if(unreported.has_key(byline)):
            unreported[byline] += 1
          else:
            unreported[byline] = 1
        else:
          gender = genderer.estimate_gender(byline)
          if(gender == None):
            gender = "N"
            unknown_count += 1
            if(unknown.has_key(byline)):
              unknown[byline] += 1
            else:
              unknown[byline] = 1
          elif(gender =="M"):
            male_count += 1
            if(male.has_key(byline)):
              male[byline] += 1
            else:
              male[byline] = 1
          elif(gender =="F"):
            female_count += 1
            if(female.has_key(byline)):
              female[byline] += 1
            else:
              female[byline] = 1

        return_row.append(gender)
    #output.writerow(return_row)

print "Total Articles," + str(total_articles)
print "Total Bylines," + str(total_bylines)
print "Unreported  Bylines," + str(unreported_count)
print "Male Bylines," + str(male_count)
print "Female Bylines," + str(female_count)
print "Unknown Bylines," + str(unknown_count)

#print unreported
#print male
#print female
#print unknown

male_output = csv.writer(open("male.csv", "wb"))
for key in male.iterkeys():
  male_output.writerow([key,male[key]])

female_output = csv.writer(open("female.csv", "wb"))
for key in female.iterkeys():
  female_output.writerow([key,female[key]])

unknown_output = csv.writer(open("unknown.csv", "wb"))
for key in unknown.iterkeys():
  unknown_output.writerow([key,unknown[key]])

unreported_output = csv.writer(open("unreported.csv", "wb"))
for key in unreported.iterkeys():
  unreported_output.writerow([key,unreported[key]])
