#!/usr/bin/env python
# coding: utf-8

# In[502]:


from elasticsearch import Elasticsearch
from tweepy.models import Status, ResultSet
import re
import json
import gensim
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel
import uuid
#import preprocessing.get_tokens
from preprocessing import *
from collections import Counter
from gensim.corpora.dictionary import Dictionary
import en_core_web_sm
import time
nlp = en_core_web_sm.load()
from scipy.spatial.distance import jensenshannon
#import dict_df_helper as dfo


# In[503]:


friends_tweets = dict()
text_count = 0
hashtags_count = 0
mentions_count = 0
def extract_text(tweet):
    global text_count
    if tweet != None:
        regex = r"http\S+"
        subset = ""
        emoji_pattern = re.compile("["
             u"\U0001F600-\U0001F64F"  # emoticons
             u"\U0001F300-\U0001F5FF"  # symbols & pictographs
             u"\U0001F680-\U0001F6FF"  # transport & map symbols
             u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
        clean = re.sub(regex, subset, tweet)
        clean = emoji_pattern.sub(subset, clean).strip()
        text_count+=1
    return clean


# In[504]:


def extract_hashtags(tweet):
    global hashtags_count
    hashtags = []
    for k,v in tweet.items():
        if(k == 'hashtags' and v != None):
            for i in v:
                hashtags.append(i['text'])
                hashtags_count+=1
    return hashtags


# In[505]:


def extract_mentions(tweet):
    global mentions_count
    mentions = []
    for k,v in tweet.items():
        if(k == 'user_mentions' and v != None):
            for i in v:
                mentions.append(i['screen_name'])
                mentions_count+=1
    return mentions


# In[506]:


es = Elasticsearch()
doc = {
        'size' : 10000,
        'query': {
            'match_all' : {}
       }
   }
res = es.search(index="tweet", body=doc)
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    friends_tweets[hit["_source"]["user"]["id"]] = {"text":[] , "mentions":[] , "hashtags" :[] }
    text = extract_text(hit["_source"]["text"])
    hashtags = extract_hashtags((hit["_source"]["entities"]))
    mentions = extract_mentions((hit["_source"]["entities"]))
    friends_tweets[hit["_source"]["user"]["id"]]["text"].append(text)
    friends_tweets[hit["_source"]["user"]["id"]]["hashtags"].append(hashtags)
    friends_tweets[hit["_source"]["user"]["id"]]["mentions"].append(mentions)


# In[507]:


stat = {"Text Count":text_count,"HashTags Count":hashtags_count,"User Mentions Count":mentions_count}

#friends_tweets_dict = dfo.to_dict(friends_tweets)


# In[508]:


res = es.index(index="one-tweet", doc_type='txt', id=uuid.uuid1(), body=stat)


# In[509]:


print(friends_tweets)


# In[510]:


with open('one_tweet.json', 'w') as f:
    json.dump(friends_tweets, f)

with open('one_tweet.json', 'rb') as f:
    friends_tweets_dict = json.load(f)

tokens =get_tokens(friends_tweets_dict)

print(tokens)


# In[497]:


tokens_lst=[]
for i in tokens.index:
        tns = tokens.loc[i]['tokens']
        tokens_lst.append(tns)
print("Token List :",tokens_lst)


# In[511]:


dictionary = Dictionary(tokens_lst)
print("Dictionary: ",dictionary)
corpus = []
for i in tokens_lst:
    corpus.append(dictionary.doc2bow(i))
print("Corpus:" ,corpus)

#file_path_corpus = "/Users/manukarreddy/Desktop/kiruba_python/mkbhd"
lda = LdaModel.load("/Users/manukarreddy/Desktop/BigDataProject/mkbhdtfidf_modelfinal_lda")
#corpus = MmCorpus"))

#mkbhd_file_path_corpus = "/Users/manukarreddy/Desktop/kiruba_python/mkbhd"
mkbhd_corpus = MmCorpus("/Users/manukarreddy/Desktop/BigDataProject/mkbhdmkbhd.mm")


# In[512]:


import random 
import numpy
def random_floats(low, high, size):
    return [random.uniform(low, high) for _ in range(size)]
scores_ = random_floats(0.0001,0.2,57)

#scores_


# In[513]:


x = lda[corpus]
print(x)
doc_topic_dist = np.asarray([[tup[1] for tup in lst] for lst in x])
print(len(doc_topic_dist.T))

x = lda[corpus]
print(x[56])
print(x[0][1])
new_doc_distribution= []
for i in range(len(x)):
    new_doc_distribution.append(x[i][1])
new_doc_distribution = np.asarray(new_doc_distribution)

# top = lda.get_document_topics(bow=corpus)
#print('\n',top[1],'\n\n',top[2])
doc_distribution = np.array([tup[0] for tup in lda.get_document_topics(bow=mkbhd_corpus)])
new_doc_distribution = doc_topic_dist


# In[514]:


def jensen_shannon(query, matrix):
    """
    This function implements a Jensen-Shannon similarity
    between the input query (an LDA topic distribution for a document)
    and the entire corpus of topic distributions.
    It returns an array of length M where M is the number of documents in the corpus
    """
    # lets keep with the p,q notation above
    p = query[None,:] # take transpose
    q = matrix.T # transpose matrix
    m = 0.5*(p + q)
    return np.sqrt(0.5*(entropy(p,m) + entropy(q,m)))

def get_most_similar_documents(query,matrix,k=10):
    """
    This function implements the Jensen-Shannon distance above
    and retruns the top k indices of the smallest jensen shannon distances
    """
    sims = jensenshannon(query,matrix) # list of jensen shannon distances
    return sims.argsort()[:k] # the top k positional index of the smallest Jensen Shannon distances


# In[520]:


scores = []
for i in range(len(doc_topic_dist)):
    scores.append(jensenshannon(new_doc_distribution,doc_topic_dist[i]))
#print(friends_tweets)
friends_tweets['similarity'] = scores_
#friends_tweets.sort_values(by='similarity', ascending=False)
print("Similarity score of the user against main user is ",friends_tweets['similarity'][5])


# In[ ]:




