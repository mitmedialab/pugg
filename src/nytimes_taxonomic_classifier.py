import yaml
import re

class NYTimesTaxonomicClassifier:
  def __init__(self, exclusion_filename, aggregation_filename):
    self.taxonomic_classifier_exclusion = yaml.load(open(exclusion_filename))
    self.taxonomic_classifier_aggregation = yaml.load(open(aggregation_filename))

  def winnow(self, taxonomic_classifiers):
    return_classifiers = []
    skip = None
    for classifier in taxonomic_classifiers:
      #exclude the classifier if it's in the exclusion list
      if classifier in self.taxonomic_classifier_exclusion:
        continue 
      #if it's in the aggregation list, add the aggregation key
      for key, aggregation_list in self.taxonomic_classifier_aggregation.items():
        if classifier in aggregation_list:
          if(key not in return_classifiers):
            return_classifiers.append(key)
          skip = True
          break

      if(not skip):
        #if it has more than three levels, do not record it
        if(re.search("/.*?/.*?/", classifier)):
          continue
        #if it has only one level, do not record it
        if not re.search("/", classifier):
          continue
        return_classifiers.append(classifier)
    return return_classifiers
