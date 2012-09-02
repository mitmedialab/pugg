from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import json
results = open("results.txt", 'w')

article_counts = {1987: 1760, \
 1988: 2099,\
 1989: 2417,\
 1990: 2778,\
 1991: 2367,\
 1992: 1749,\
 1993: 1812,\
 1994: 1578,\
 1995: 1684,\
 1996: 1513,\
 1997: 1363,\
 1998: 1270,\
 1999: 1282,\
 2000: 1230,\
 2001: 1071,\
 2002: 1048,\
 2003: 915,\
 2004: 801,\
 2005: 862,\
 2006: 850}

tot_words = {1987: 0, \
             1988: 0, \
             1989: 0, \
             1990: 0, \
             1991: 0, \
             1992: 0, \
             1993: 0, \
             1994: 0, \
             1995: 0, \
             1996: 0, \
             1997: 0, \
             1998: 0, \
             1999: 0, \
             2000: 0, \
             2001: 0, \
             2002: 0, \
             2003: 0, \
             2004: 0, \
             2005: 0, \
             2006: 0}

for i in range(1987,2007):
    for j in range(article_counts[i]):
        current_file = open("obits_mal/"+str(i)+'/'\
                            +str(j)+'.txt', 'r')
        fulltext = current_file.read()
        for sent in sent_tokenize(fulltext):
            for word in word_tokenize(sent):
                tot_words[i] += 1
        current_file.close()
results.write(json.dumps(tot_words))
results.close()

