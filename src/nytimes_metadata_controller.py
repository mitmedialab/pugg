from name_gender import *
from pronoun_gender import *
from nytimes_article import *
from nytimes_article_accessor import *
from nytimes_taxonomic_classifier import *
from decimal import *
import sys
import re

class NYTimesMetadataController:
  def __init__(self):
    self.articles = NYTimesArticleAccessor("data/nytimes")
    self.name_gender = NameGender("data/names/female_names_EN_US.csv", "data/names/male_names_EN_US.csv")
    self.pronoun_gender = PronounGender("data/pronouns/female-EN.csv", "data/pronouns/male-EN.csv", "data/pronouns/neutral-EN.csv")

  def saveToMongoDB(self):
    article_row = self.articles.getNextArticle()
    year = 0
    while article_row:
      try:
        article = self.articles.createArticle(article_row)
      except ValueError:
        article_row = self.articles.getNextArticle()
        continue
      article.save()
      if(article.pub_date.month == 1 and year < article.pub_date.year):
        print year
        year = article.pub_date.year
      article_row = self.articles.getNextArticle()

 
  def generate_yearly_gender_counts(self):
    total = female = male = unknown = unlabeled = 0 
    print "@year, @total, @female, @male, @unknown, @unlabeled"

    article_row = self.articles.getNextArticle()
    year = 0
    while article_row:
      try:
        article = self.articles.createArticle(article_row)
      except ValueError:
        article_row = self.articles.getNextArticle()
        continue
      if(year + 1 == article.pub_date.year and total > 0 ):
        print str(year) + "," + str(total) + "," + str(female) + "," + str(male) + "," + str(unknown) + "," + str(unlabeled)
        sys.stdout.flush()
        total = female = male = unknown = unlabeled = 0 
      year = article.pub_date.year

      total += 1
      article_gender = self.name_gender.estimate_gender(article.byline)
      if article_gender == "F":
        female += 1
      elif article_gender == "M":
        male += 1
      else: 
        if(len(article.byline) >0 and article.byline != "ap" and 
          article.byline != "special to the new york times" and 
          article.byline!="reuters" and article.byline !="the associated press"):
          #print article.byline
          unknown += 1
        else:
          unlabeled += 1
      article_row = self.articles.getNextArticle()
    print str(year) + "," + str(total) + "," + str(female) + "," + str(male) + "," + str(unknown) + "," + str(unlabeled)
 
  def increment_gender_dict(self, gender_dict, key, pronoun_result):
    if pronoun_result == "M":
      gender_dict[key]["subject_male"] += 1
    elif pronoun_result == "N":
      gender_dict[key]["subject_middle"] += 1
    elif pronoun_result == "F":
      gender_dict[key]["subject_female"] += 1

  def initialize_gender_dict(self, dictionary):
      dictionary["total"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
      dictionary["female"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
      dictionary["male"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
      dictionary["unknown"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
      dictionary["unlabeled"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
    
  def generate_monthly_gender_counts(self):
    header =  "@date, @classifier, @total, @female, @female_subject_male, @female_subject_female, @female_subject_middle, @female_subject_male_percent, @female_subject_female_percent, @female_subject_middle_percent, @male, @male_subject_male, @male_subject_female, @male_subject_middle, @male_subject_male_percent, @male_subject_female_percent, @male_subject_middle_percent, @unknown, @unknown_subject_male, @unknown_subject_female, @unknown_subject_middle, @unknown_subject_male_percent, @unknown_subect_female_percent, @unknown_subject_middle_percent, @unlabeled, @unlabeled_subject_male, @unlabeled_subject_female, @unlabeled_subject_middle, @unlabeled_subject_male_percent, @unlabeled_subject_female_percent, @unlabeled_subject_middle_percent"
    print header
    articles = self.articles.getNextMonth()
    getcontext.prec = 4

    nyt_classifier = NYTimesTaxonomicClassifier("data/utility-data/nytimes_taxonomic_classifier_exclusion.yml", "data/utility-data/nytimes_taxonomic_classifier_aggregation.yml")
    
    while articles:
      if(self.articles.createArticle(articles[0]).pub_date.year < 1997):
        articles = self.articles.getNextMonth()
        continue
      monthly_counts = {}
      monthly_counts["all"] = {}
      self.initialize_gender_dict(monthly_counts["all"])
        
      for article_row in articles:
        try:
          article = self.articles.createArticle(article_row)
          fulltext = article.getDataFileObject("data/full/", "data/nytimes-fulltext/", "txt").read()
        except ValueError:
          continue

        article_gender = self.name_gender.estimate_gender(article.byline)
        subject_gender = self.pronoun_gender.estimate_gender(fulltext)
        gender_key = ""
        if article_gender == "F":
          gender_key = "female"
        elif article_gender == "M":
          gender_key = "male"
        else: 
          if len(article.byline) >0 and article.byline != "ap" and article.byline != "special to the new york times" and article.byline!="reuters" and article.byline !="the associated press":
            #print article.byline
            gender_key="unknown"
          else:
            gender_key = "unlabeled"

        monthly_counts["all"]["total"]["bylines"] += 1
        monthly_counts["all"][gender_key]["bylines"] += 1
        self.increment_gender_dict(monthly_counts["all"], gender_key, subject_gender)

        for classifier in nyt_classifier.winnow(article.taxonomic_classifiers):
          if classifier not in monthly_counts:
            monthly_counts[classifier] = {}
            self.initialize_gender_dict(monthly_counts[classifier])

          monthly_counts[classifier]["total"]["bylines"] += 1
          monthly_counts[classifier][gender_key]["bylines"] += 1
          self.increment_gender_dict(monthly_counts[classifier], gender_key, subject_gender)

      #for every month, print CSV line
      date = str(article.pub_date.month) + "/" + str(article.pub_date.year)
      for classifier, gender in monthly_counts.items():
        csv_line = "01/" + date + "," + re.sub(",",".", classifier)
        for key in ["total", "female", "male", "unknown", "unlabeled"]:
          csv_line += "," + str(gender[key]["bylines"]) 
          try: 
            if(key!="total"):
              subject_total = float(gender[key]["subject_male"] + gender[key]["subject_female"] + gender[key]["subject_middle"])
              if(subject_total == 0):
                csv_line += ", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
                continue
              csv_line += "," + str(gender[key]["subject_male"]) 
              csv_line += "," + str(gender[key]["subject_female"])
              csv_line += "," + str(gender[key]["subject_middle"])
              csv_line += "," + str(Decimal(Decimal(gender[key]["subject_male"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
              csv_line += "," + str(Decimal(Decimal(gender[key]["subject_female"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
              csv_line += "," + str(Decimal(Decimal(gender[key]["subject_middle"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
          except:
            import pdb;pdb.set_trace()

        print csv_line
      articles = self.articles.getNextMonth()

  def increment_gender_dict_monthObit(self, gender_dict, pronoun_result):
    if pronoun_result == "M":
      gender_dict["subject_male"] += 1
    elif pronoun_result == "N":
      gender_dict["subject_middle"] += 1
    elif pronoun_result == "F":
      gender_dict["subject_female"] += 1
    
  def generate_monthly_obituary_counts(self):
    header =  "@date, @total, @subject_female, @subject_male, @subject_middle, @subject_female_percent, @subject_male_percent, @subject_middle_percent"
    print header
    articles = self.articles.getNextMonth()
    getcontext.prec = 4

    nyt_classifier = NYTimesTaxonomicClassifier("data/utility-data/nytimes_taxonomic_classifier_exclusion.yml", "data/utility-data/nytimes_taxonomic_classifier_aggregation.yml")
    
    while articles:
      monthly_counts = {"total": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
        
      for article_row in articles:
        try:
          article = self.articles.createArticle(article_row)
          fulltext = article.getDataFileObject("data/nytimes/", "data/nytimes-fulltext/", "txt").read()
        except ValueError:
          continue

        # Only increment monthly_counts for obituaries
        if "Death" in nyt_classifier.winnow(article.taxonomic_classifiers): #"Death" for obits & paid death notices, "Death_unpaid" for just obits.
            subject_gender = self.pronoun_gender.estimate_gender(fulltext)

            monthly_counts["total"] += 1
            self.increment_gender_dict_monthObit(monthly_counts, subject_gender)

      #for every month, print CSV line
      date = str(article.pub_date.month) + "/" + str(article.pub_date.year)
      csv_line = date
      csv_line += "," + str(monthly_counts["total"])
      subject_total = float(monthly_counts["subject_female"] + monthly_counts["subject_male"] + monthly_counts["subject_middle"])
      if(subject_total == 0):
          csv_line += ", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0"
      else:
        csv_line += "," + str(monthly_counts["subject_female"])
        csv_line += "," + str(monthly_counts["subject_male"])
        csv_line += "," + str(monthly_counts["subject_middle"])
        csv_line += "," + str(Decimal(Decimal(monthly_counts["subject_female"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
        csv_line += "," + str(Decimal(Decimal(monthly_counts["subject_male"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
        csv_line += "," + str(Decimal(Decimal(monthly_counts["subject_middle"]) / Decimal(subject_total)).quantize(Decimal("0.0001"), rounding=ROUND_UP))
      
      print csv_line
      articles = self.articles.getNextMonth()

  def generate_obituary_fulltext_samples(self):
    
    monthID = 0

    filename_female = "female0.txt"
    filename_male = "male0.txt"
    filename_middle = "middle0.txt"

    file_female = open("fulltext_samples/" + filename_female, 'w')
    file_male = open("fulltext_samples/" + filename_male, 'w')
    file_middle = open("fulltext_samples/" + filename_middle, 'w')
    
    articles = self.articles.getNextMonth()
    getcontext.prec = 4

    nyt_classifier = NYTimesTaxonomicClassifier("data/utility-data/nytimes_taxonomic_classifier_exclusion.yml", "data/utility-data/nytimes_taxonomic_classifier_aggregation.yml")
    
    while articles:
      if(self.articles.createArticle(articles[0]).pub_date.year < 1997):
        articles = self.articles.getNextMonth()
        continue
        
      for article_row in articles:
        try:
          article = self.articles.createArticle(article_row)
          fulltext = article.getDataFileObject("data/nytimes/", "data/nytimes-fulltext/", "txt").read()
        except ValueError:
          continue

        # Only increment monthly_counts for obituaries
        if "Death" in nyt_classifier.winnow(article.taxonomic_classifiers):
            subject_gender = self.pronoun_gender.estimate_gender(fulltext)
            read_to_char_index = min(300, len(fulltext))
            if subject_gender == "F":
              file_female.write(re.sub('\n',' ',fulltext[:read_to_char_index])+'\n')
            if subject_gender == "M":
              file_male.write(re.sub('\n',' ',fulltext[:read_to_char_index])+'\n')
            if subject_gender == "N":
              file_middle.write(re.sub('\n',' ',fulltext[:read_to_char_index])+'\n')

      monthID += 1

      file_female.close()
      file_male.close()
      file_middle.close()

      filename_female = "female" + str(monthID) + ".txt"
      filename_male = "male" + str(monthID) + ".txt"
      filename_middle = "middle" + str(monthID) + ".txt"

      file_female = open("fulltext_samples/" + filename_female, 'w')
      file_male = open("fulltext_samples/" + filename_male, 'w')
      file_middle = open("fulltext_samples/" + filename_middle, 'w')
      articles = self.articles.getNextMonth()


if __name__ == "__main__":
    nyt_controller = NYTimesMetadataController()
    nyt_controller.generate_obituary_fulltext_samples()
    #nyt_controller.saveToMongoDB()

