from tweepy import OAuthHandler
import json
import configparser
import random
import tweepy
import pickle
import json
import os
from tweepy.models import Status, ResultSet
import re

def get_twitter(config_file):
    print("Reading config file:")
    config= configparser.ConfigParser()
    config.read(config_file)
    auth = tweepy.AppAuthHandler(config.get('twitter', 'consumer_key'),config.get('twitter', 'consumer_secret') ) 
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print("Established Twitter Connection Successfully!")
    return auth, api

def get_friends(user,count=None):
    friends = []
    if count == None:
        for friend in tweepy.Cursor(api.friends, screen_name=user).items():
            friends.append(friend.screen_name)
        friends = list(set(friends))
    else:
        for friend in tweepy.Cursor(api.friends, screen_name=user,count = count).items(count):
            friends.append(friend.screen_name)
        friends = list(set(friends))
    return friends

def get_deg2_users(friends, count):
    friendsd2 = set()
    backoff_counter = 1
    ct=0
    for f in friends: 
        try:
            print("Getting friends of : ",f)
            for x in (get_friends(f,count)):
                print("Adding ",x)
                friendsd2.add(x)
            #d1.pop(0)
            ct+=1
            print("%d of %d remaining......."%((len(friends) - ct),len(friends)))
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(20)
            backoff_counter += 1
            continue
    return list(friendsd2)


def extract_text(tweet):
    if type(tweet) != Status:
        print("Please enter in a tweet of type Status")
        return []
    else:

        regex = r"http\S+"
        subset = ""

        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

        if hasattr(tweet, "full_text"):
            clean = re.sub(regex, subset, tweet.full_text.strip())
            clean = emoji_pattern.sub(subset, clean).strip()
        return clean

def extract_mentions(tweet):

    mentions = []
    if type(tweet) != Status:
        print("Please enter in a tweet of type Status")
        return []
    else:
        if hasattr(tweet, "entities"):
            if tweet.entities['user_mentions'] == []:
                return []
            else:
                for i in tweet.entities['user_mentions']:
                    mentions.append(i['screen_name'])
        else:
            print("No entity method!")
        return mentions

def extract_hashtags(tweet):

    hashtags = []
    if type(tweet) != Status:
        print("Please enter in a tweet of type Status")
        return []
    else:
        if hasattr(tweet, "entities"):
            if tweet.entities['hashtags'] == []:
                return []
            else:
                for i in tweet.entities['hashtags']:
                    hashtags.append(i['text'])
        else:
            print("No entity method!")
        return hashtags

def main_tweets(user):
    m_tweets =dict()
    m_tweets[user] = {"text":[] , "mentions":[] , "hashtags" :[] }
    tweets = []
    try:
        for status in tweepy.Cursor(api.user_timeline, screen_name =user, tweet_mode = "extended", include_rts=False).items():
            tweets.append(status)
        for tweet in tweets:
            text = extract_text(tweet) 
            hashtags = extract_hashtags(tweet) 
            mentions = extract_mentions(tweet)
            m_tweets[user]["text"].append(text)
            m_tweets[user]["hashtags"].append(hashtags)
            m_tweets[user]["mentions"].append(mentions)
    except Exception as e:
        if (str(e) == "Twitter error response: status code = 401"):
            print("user is protected")
            tweets = []
        elif (str(e) == "Twitter error response: status code = 404"):
            print("user is not found")
            tweets = []
        else:
            print(str(e))
    print("Finished Getting tweets....")
    return m_tweets

def fetch_tweets(users):
    friends_tweets = dict()
    i = 1
    protected = 0
    not_found = 0
    for user in users:
        friends_tweets[user] = {"text":[] , "mentions":[] , "hashtags" :[] }
        print("Getting 200 tweets of :", user)
        print("%d remaining...."%(len(users)-i))
        tweets = []
        try:
            for status in tweepy.Cursor(api.user_timeline, screen_name =user, tweet_mode = "extended", count = 200, include_rts=False).items(200):
                tweets.append(status)
            i+=1
            for tweet in tweets:
                text = extract_text(tweet) 
                hashtags = extract_hashtags(tweet) 
                mentions = extract_mentions(tweet)
                friends_tweets[user]["text"].append(text)
                friends_tweets[user]["hashtags"].append(hashtags)
                friends_tweets[user]["mentions"].append(mentions)
        except Exception as e:
            if (str(e) == "Twitter error response: status code = 401"):
                print("user is protected")
                protected+=1
                tweets = []
            elif (str(e) == "Twitter error response: status code = 404"):
                print("user is not found")
                not_found+=1
                tweets = []
            else:
                print(str(e))
    print("Finished Getting tweets....")
    print("Number of protected users: ",protected)
    print("Number of accounts not found: ", not_found)
    return friends_tweets, protected, not_found

def save_json(file, name, path):
    with open(path+"{}.mm".format(name), 'w') as fp:
        json.dump(file, fp)
        
def save_pkl(file, name, path):
    with open(path+"{}.mm".format(name), 'wb') as f:
        pickle.dump(file, f)