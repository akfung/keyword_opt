import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

df_private = pd.read_csv("private_db.csv")
df_public = pd.read_csv("public_database.csv")

# update list of stopwords from nltk
stop_words = set(stopwords.words('english'))
# remove some common terms used in pubmed abstract
stop_words.update(['background', 'methods', 'results', 'conclusions'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
# function to remove stop words


def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)


'''
Creates data frame with unique words from given keywords
'''
# df to hold word and number of occurances
keywords = pd.DataFrame(columns=['keyword', 'occurances'])
keywords = np.array(['keyword', 'occurances'])
word_index = 1  # index to track progress of adding words

# check if each word is already in df, add if not present
for entry in df_public.head(100)['keywords']:
    word_bag = str(entry).split('; ')
    for word in word_bag:
        if not(word.lower in list(keywords['keyword'])):
            # add word with 0 initial occurances
            keywords.loc[-1] = [word.lower(), 0]
            keywords.index = keywords.index + 1
            if word_index % 1000 == 0:  # display progress every 1000
                print("Adding word " + str(word_index))
            word_index += 1
