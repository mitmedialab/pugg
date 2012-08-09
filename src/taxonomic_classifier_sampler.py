from nytimes_article import *
from nytimes_article_accessor import *

class NYTimesTaxClassSampler:
    def __init__(self):
        self.articles = NYTimesArticleAccessor("data/nytimes")

    def generate_tax_class_samples(self):
        tax_class_samples = []
        article_row = self.articles.getNextArticle()
        year = 0
        
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

if __name__ == "__main__":
    nyt_tax_class_sampler = NYTimesTaxClassSampler()
    nyt_tax_class_sampler.generate_tax_class_samples()
