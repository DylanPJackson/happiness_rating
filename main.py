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
from tweepy import OAuthHandler, Stream, API, Cursor

import twitter_credentials
import numpy as np
import pandas as pd

# For specific user interaction
class TwitterClient():
    def __init__(self, twitter_user):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)    
        self.twitter_user = twitter_user
    
    # Gets specified number of tweets from user
    def get_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets 

# Class for general Twitter authentication
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, 
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, 
                                twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# Class for streaming and processing live tweets
class TwitterStreamer():
    # Constructor
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()   
 
    # Handles Twitter authentication and connection to Twitter Streaming API
    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):      
        listener = TwitterListener(fetched_tweet_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)
    
    
# Basic listener class that just prints received tweets to stdout 
class TwitterListener(StreamListener):
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
        # If we are throttling Twitter API
        if status == 420:
            return False
        print(status)
        
if __name__ == "__main__":
    """
        TODO : Prompt user for hashtags to look up rather than hardcode it
        TODO : Prompt user for twitter handle to analyse
    """
    
    """
        First four lines return live tweets from given hashtags. 
        Last two return specified number of tweets from specified user        

    hash_tag_list = ["overwatch", "league of legends", "dota", "cs:go"]
    fetched_tweets_filename = "tweets.json"
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list) 
    
    twitter_client = TwitterClient('realDonaldTrump')
    print(twitter_client.get_tweets(1)[0].text)
    """
