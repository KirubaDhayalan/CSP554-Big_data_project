#!/usr/bin/env python
# coding: utf-8

# In[31]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient
from elasticsearch import Elasticsearch
import uuid
import json
#twitterid = sys.argv[1]

var = input("Please Enter Twitter ID: ")

access_token = "1163906181326393344-CJ3UW5OpOXQ5Z0xU3VbldPgNB74LWw"
access_token_secret =  "TynADcZzVYw1kCaGeJcUhumbc22EVk6tqghTIRf5FQxYk"
consumer_key =  "5zVc2FLknf7p0Rh0nyh6IJr2v"
consumer_secret =  "xBMYKqlqdWbLIbpBbZl0Nw8Mr5wtUlve78n470cFe7crHyAE0d"

class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages("bigdataproject", data.encode('utf-8'))
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        res = es.index(index="tweet", doc_type='tweet', id=uuid.uuid1(), body=data)
        print(res['result'])
        #print(es.search(index='test-tweet'))
        with open('tweets.json', 'a') as tf:
            #Write a new line
            tf.write('\n')

            #Write the json data directly to the file
            json.dump(data, tf)
            #Alternatively: tf.write(json.dumps(all_data))
        #print (data)
        return True
    def on_error(self, status):
        print (status)

kafka = KafkaClient("localhost:9092")
producer = SimpleProducer(kafka)
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)
stream.filter(follow=[var])


# In[ ]:




