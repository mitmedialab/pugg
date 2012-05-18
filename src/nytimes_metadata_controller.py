from name_gender import *
from pronoun_gender import *
from nytimes_article import *
from nytimes_article_accessor import *
import sys

class NYTimesMetadataController:
  def __init__(self):
    self.articles = NYTimesArticleAccessor("data/nytimes")
    self.name_gender = NameGender("data/names/female_names.csv", "data/names/male_names.csv")
    self.pronoun_gender = PronounGender("data/pronouns/female-EN.csv", "data/pronouns/male-EN.csv")

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
    
  def generate_monthly_gender_counts(self):
    header =  "@date, @total, @total_subject_male, @total_subject_female, @total_subject_middle, @female, @female_subject_male, @female_subject_female, @female_subject_middle, @male, @male_subject_male, @male_subject_female, @male_subject_middle, @unknown, @unknown_subject_male, @unknown_subject_female, @unknown_subject_middle, @unlabeled, @unlabeled_subject_male, @unlabeled_subject_female, @unlabeled_subject_middle"
    print header
    articles = self.articles.getNextMonth()
    gender = {}
    while articles:
      gender["total"] = gender["female"] = gender["male"] = gender["unknown"] = gender["unlabeled"] = {"bylines": 0, "subject_male": 0, "subject_middle": 0, "subject_female": 0}
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

        gender["total"]["bylines"] += 1
        gender[gender_key]["bylines"] += 1
        self.increment_gender_dict(gender, gender_key, subject_gender)

      #for every month, print CSV line
      date = str(article.pub_date.month) + "/" + str(article.pub_date.year)
      ##csv_line = "01/" + date + "," + str(gender["total"]["bylines"]) + "," + str(gender["female"]["bylines"]) + "," + str(gender["male"]["bylines"]) + "," + str(gender["unknown"]["bylines"]) + "," + str(gender["unlabeled"]["bylines"])
      csv_line = "01/" + date 
      for key in ["total", "female", "male", "unknown", "unlabeled"]:
        csv_line += "," + str(gender[key]["bylines"]) + "," + str(gender[key]["subject_male"]) + "," + str(gender[key]["subject_female"]) + "," + str(gender[key]["subject_middle"])
      print csv_line
      articles = self.articles.getNextMonth()

if __name__ == "__main__":
    nyt_controller = NYTimesMetadataController()
    nyt_controller.generate_monthly_gender_counts()
    #nyt_controller.saveToMongoDB()
