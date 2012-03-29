from name_gender import *
from nytimes_article import *
from nytimes_article_accessor import *
import sys

class NYTimesMetadataController:
  def __init__(self):
    self.articles = NYTimesArticleAccessor("data/nytimes")
    self.name_gender = NameGender("data/names/female_names.csv", "data/names/male_names.csv")

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
 
  def generate_monthly_gender_counts(self):
    print "@date, @total, @female, @male, @unknown, @unlabeled"
    articles = self.articles.getNextMonth()
    while articles:
      female = 0
      male = 0
      unknown = 0
      unlabeled = 0
      total = 0 
      for article_row in articles:
        try:
          article = self.articles.createArticle(article_row)
        except ValueError:
          continue

        total += 1

        article_gender = self.name_gender.estimate_gender(article.byline)
        if article_gender == "F":
          female += 1
        elif article_gender == "M":
          male += 1
        else: 
          if len(article.byline) >0 and article.byline != "ap" and article.byline != "special to the new york times" and article.byline!="reuters" and article.byline !="the associated press":
            #print article.byline
            unknown += 1
          else:
            unlabeled += 1
      date = str(article.pub_date.month) + "/" + str(article.pub_date.year)
      print "01/" + date + "," + str(total) + "," + str(female) + "," + str(male) + "," + str(unknown) + "," + str(unlabeled)
      articles = self.articles.getNextMonth()

if __name__ == "__main__":
    nyt_controller = NYTimesMetadataController()
    #nyt_controller.generate_yearly_gender_counts()
    nyt_controller.saveAllToRedis()
