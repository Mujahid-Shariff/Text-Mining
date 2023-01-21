# -*- coding: utf-8 -*-
"""Text Mining.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OkQ5wRs371gMCSQMrj7PzCRP_eSq4RVE

Text Mining assignment

ONE: 1) Perform sentimental analysis on the Elon musk tweets (Elon_musk.csv)

TWO: 1) Extract reviews of any product from ecommerce website like amazon.      
               2) Perform emotion mining.
"""

from  google.colab import files
uploaded  = files.upload()

# Import the data
import pandas as pd
data = pd.read_csv('Elon_musk.csv', encoding="latin1")
data.head()

# Number of Words in single tweet
data['word_count'] = data['Text'].apply(lambda x: len(str(x).split(" ")))
data[['Text','word_count']].head()

# Number of characters in single tweet
data['char_count'] = data['Text'].str.len() # this also includes spaces
data[['Text','char_count']].head()

# Average Word Length
def avg_word(sentence):
  words = sentence.split()
  return (sum(len(word) for word in words)/len(words))

data['avg_word'] = data['Text'].apply(lambda x: avg_word(x))
data[['Text','avg_word']].head()

import nltk
nltk.download('stopwords')

nltk.download('wordnet')

pip install -U textblob

# Number of stopwords
from nltk.corpus import stopwords
stop = stopwords.words('english')

data['stopwords'] = data['Text'].apply(lambda x: len([x for x in x.split() if x in stop]))
data[['Text','stopwords']].head()

# Number of Special Characters
data['hastags'] = data['Text'].apply(lambda x: len([x for x in x.split() if x.startswith('@')]))
data[['Text','hastags']].head()

# Number of Upper Case Words
data['upper'] = data['Text'].apply(lambda x: len([x for x in x.split() if x.isupper()]))
data[['Text','upper']].head()

"""**Pre-Processing**"""

# Lower Case
data['Text'] = data['Text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
data['Text'].head()

# Removing Punctuation
data['Text'] = data['Text'].str.replace('[^\w\s]','')
data['Text'].head()

# Removal of Stop Words
stop = stopwords.words('english')
data['Text'] = data['Text'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
data['Text'].head()

# Common word removal
freq = pd.Series(' '.join(data['Text']).split()).value_counts()[:10]
freq

freq = list(freq.index)
data['Text'] = data['Text'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
data['Text'].head()

# Rare Words Removal
freq = pd.Series(' '.join(data['Text']).split()).value_counts()[-10:]
freq

freq = list(freq.index)
data['Text'] = data['Text'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
data['Text'].head()

# Spelling correction
from textblob import TextBlob
data['Text'][:5].apply(lambda x: str(TextBlob(x).correct()))

nltk.download('punkt')

# Tokenization
TextBlob(data['Text'][1]).words

# Stemming
from nltk.stem import PorterStemmer
st = PorterStemmer()
data['Text'][:5].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))

"""**Advanced Text Processing**"""

# N-grams
TextBlob(data['Text'][0]).ngrams(2)

# Term frequency
tf1 = (data['Text'][1:2]).apply(lambda x: pd.value_counts(x.split(" "))).sum(axis = 0).reset_index()
tf1.columns = ['words','tf']
tf1

# Inverse Document Frequency
import numpy as np
for i,word in enumerate(tf1['words']):
  tf1.loc[i, 'idf'] = np.log(data.shape[0]/(len(data[data['Text'].str.contains(word)])))

tf1

# Term Frequency – Inverse Document Frequency (TF-IDF)
tf1['tfidf'] = tf1['tf'] * tf1['idf']
tf1

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=1000, lowercase=True, analyzer='word',
 stop_words= 'english',ngram_range=(1,1))
vect = tfidf.fit_transform(data['Text'])
vect

# Bag of Words
from sklearn.feature_extraction.text import CountVectorizer
bow = CountVectorizer(max_features=1000, lowercase=True, ngram_range=(1,1),analyzer = "word")
data_bow = bow.fit_transform(data['Text'])
data_bow

# Sentiment Analysis
data['Text'][:5].apply(lambda x: TextBlob(x).sentiment)

data['sentiment'] = data['Text'].apply(lambda x: TextBlob(x).sentiment[0] )
data[['Text','sentiment']].head()


# Joining the list into one string/text
text = ' '.join(data['Text'])
text

# Commented out IPython magic to ensure Python compatibility.
#  Generate wordcloud
import matplotlib.pyplot as plt
# %matplotlib inline
from wordcloud import WordCloud
from wordcloud import WordCloud, STOPWORDS
# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(15, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off");

# Generate wordcloud
stopwords = STOPWORDS
stopwords.add('will')
stopwords.add('apple')
stopwords.add('Amazon')
stopwords.add('laptop')
    
wordcloud = WordCloud(width = 3000, height = 2000, background_color='black', max_words=100,colormap='Set2',stopwords=stopwords).generate(text)

# Plot
plot_cloud(wordcloud)
