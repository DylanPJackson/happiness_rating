"""
    filename:
        main.py
    
    description:
        Handles streaming live tweets and performing sentiment analysis on them
    
    author:
        Dylan P. Jackson

    references:
        vprusso 
"""

# Allows to listen to specified tweets as they are posted
from tweepy.streaming import StreamListener
# Authenticates based off of credentials stored in twitter_credentials 
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials

# Class for streaming and processing live tweets
class TwitterStreamer():
    
    # Handles Twitter authentication and connection to Twitter Streaming API
    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):      
        listener = StdOutListener(fetched_tweet_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, 
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, 
                                twitter_credentials.ACCESS_TOKEN_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)
    
    
# Basic listener class that just prints received tweets to stdout 
class StdOutListener(StreamListener):
    # Constructor
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    # Overriden method which takes in data streamed in from StreamListener
    def on_data(self, data):
        try:
            print(data)
            # Alternatively write output to given file 
            """with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True""" 
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True       

    # Overriden method which happens if error occurs
    def on_error(self, status):
        print(status)
        
if __name__ == "__main__":
    hash_tag_list = ["overwatch", "league of legends", "dota", "cs:go"]
    fetched_tweets_filename = "tweets.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list) 
