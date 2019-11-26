#!/usr/bin/env python
# coding: utf-8

# In[115]:


import pickle
import nltk
import pandas as pd
import numpy as np
import tweepy
import re
import json
from tweepy.models import Status
import pandas as pd
import string
from nltk.corpus import stopwords

nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]

def get_df(dict):
    df = pd.DataFrame.from_dict(dict, orient='index')
    return df

def filtration(dataframe, column):
    for handle in dataframe.index:
        for index, tweet in enumerate(dataframe.loc[handle, :][column]):
            tweet = tweet.lower()
            clean = [x for x in tweet.split() if x not in string.punctuation]
            clean = [x for x in clean if x not in nltk_stopwords]
            #clean = re.sub(r'\b\w{1,3}\b', '', clean)
            clean = [x for x in clean if "@" not in x]
            clean = [x for x in clean if "…" not in x]
            clean = [x for x in clean if x[0] not in string.digits]
            clean = [x for x in clean if x[0] not in string.punctuation]
            clean = list(map(lambda x: x.replace("#", ""), clean))
            clean = list(map(lambda x: x.replace('"', ""), clean))
            clean = list(map(lambda x: x.replace(".",""), clean))
            clean = list(map(lambda x: x.replace("-&gt;", ""), clean))
            clean = list(map(lambda x: x.replace("&gt;", "greater than"), clean))
            clean = list(map(lambda x: x.replace("&lt;", "less than"), clean))
            clean = list(map(lambda x: x.replace(":", ""), clean))
            clean = list(map(lambda x: x.replace("&amp;", "&"), clean))
            clean = list(map(lambda x: x.replace("/", ""), clean))
            clean = list(map(lambda x: x.replace("...", ""), clean))
            clean = list(map(lambda x: x.replace("(", ""), clean))
            clean = list(map(lambda x: x.replace(")", ""), clean))
            clean = list(map(lambda x: x.replace("“", '"'), clean))
            clean = list(map(lambda x: x.replace("”", '"'), clean))
            clean = list(map(lambda x: x.replace("’", ""), clean))
            clean = list(map(lambda x: x.replace("-"," "), clean))
            clean = list(map(lambda x: x.replace("*", ""), clean))
            clean = list(map(lambda x: x.replace("!", ""), clean))
            clean = list(map(lambda x: x.replace("⬛️", ""), clean))
            clean = list(map(lambda x: x.replace("\u200d", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f986", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f942", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f92f", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f911", ""), clean))
            clean = list(map(lambda x: x.replace("[", ""), clean))
            clean = list(map(lambda x: x.replace("]", ""), clean))
            clean = list(map(lambda x: x.replace("{", ""), clean))
            clean = list(map(lambda x: x.replace("}", ""), clean))
            clean = list(map(lambda x: x.replace("ô", "o"), clean))
            clean = list(map(lambda x: x.replace("ó", "o"), clean))
            clean = list(map(lambda x: x.replace("é", "e"), clean))
            clean = list(map(lambda x: x.replace("ï","i"), clean))
            clean = list(map(lambda x: x.replace("®", ""), clean))
            clean = list(map(lambda x: x.replace("á", "a"), clean))
            clean = list(map(lambda x: x.replace("ã", "a"), clean))
            clean = list(map(lambda x: x.replace("ç", "c"), clean))
            clean = list(map(lambda x: x.replace("$", ""), clean))
            clean = list(map(lambda x: x.replace("'ve", ""), clean))
            clean = list(map(lambda x: x.replace("'ll", ""), clean))
            clean = list(map(lambda x: x.replace("n't", ""), clean))
            clean = list(map(lambda x: x.replace("'re", ""), clean))
            clean = list(map(lambda x: x.replace("l'", ""), clean))
            clean = list(map(lambda x: x.replace("?i", ""), clean))
            clean = " ".join(clean)
            dataframe.loc[handle, :][column][index] = clean
    return dataframe


def to_dict(dataframe):
    temp_dict = dict()
    for handle in dataframe.index:
        temp_dict[handle] = pd.Series.to_dict(dataframe.loc[handle, :])
    return temp_dict

