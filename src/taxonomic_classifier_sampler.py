from nytimes_article import *
from nytimes_article_accessor import *

class NYTimesTaxClassSampler:
    def __init__(self):
        self.articles = NYTimesArticleAccessor("data/nytimes")

    def generate_tax_class_samples(self):
        tax_class_samples = []
        article_row = self.articles.getNextArticle()
        
        while article_row:
          try:
              article = self.articles.createArticle(article_row)
          except ValueError:
              article_row = self.articles.getNextArticle()
              continue
          for tax_class in article.taxonomic_classifiers:
              if tax_class not in tax_class_samples:
                  tax_class_samples.append(tax_class)
          article_row = self.articles.getNextArticle()

        for tax_class in tax_class_samples:
            print tax_class

    def generate_classifier_count(self):
        obit_count = 0
        movies_obit_count = 0
        
        article_row = self.articles.getNextArticle()
        
        while article_row:
          try:
              article = self.articles.createArticle(article_row)
          except ValueError:
              article_row = self.articles.getNextArticle()
              continue
          for tax_class in article.taxonomic_classifiers:
              if tax_class == "Top/News/Obituaries":
                  obit_count += 1
              if tax_class == "Top/Features/Movies/News and Features/Obituaries":
                  movies_obit_count += 1
          article_row = self.articles.getNextArticle()

        print "Top/News/Obituaries: " + str(obit_count)
        print "Top/Features/Movies/News and Features/Obituaries: " + str(movies_obit_count)

if __name__ == "__main__":
    nyt_tax_class_sampler = NYTimesTaxClassSampler()
    nyt_tax_class_sampler.generate_classifier_count()
