#!/usr/bin/env python
# coding: utf-8

# In[30]:


from elasticsearch import Elasticsearch
from tweepy.models import Status, ResultSet
import re
import json
import uuid
import preprocessing.get_tokens


# In[25]:


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
def extract_hashtags(tweet):
    global hashtags_count
    hashtags = []
    for k,v in tweet.items():
        if(k == 'hashtags' and v != None):
            for i in v:
                hashtags.append(i['text'])
                hashtags_count+=1
    return hashtags

def extract_mentions(tweet):
    global mentions_count
    mentions = []
    for k,v in tweet.items():
        if(k == 'user_mentions' and v != None):
            for i in v:
                mentions.append(i['screen_name'])
                mentions_count+=1
    return mentions

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


# In[32]:


stat = {"Text Count":text_count,"HashTags Count":hashtags_count,"User Mentions Count":mentions_count}


# In[37]:


res = es.index(index="one-tweet", doc_type='txt', id=uuid.uuid1(), body=stat)


# In[27]:


print(friends_tweets)


# In[34]:


with open('one_tweet.json', 'w') as f:
    json.dump(friends_tweets, f)

tokens_df = get_tokens(friends_tweets)


