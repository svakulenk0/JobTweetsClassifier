#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 30, 2017
.. codeauthor: svitlana vakulenko
<svitlana.vakulenko@gmail.com>

Classifies tweets in real time
'''
from tweepy.streaming import StreamListener
from tweepy import Stream, API, OAuthHandler

from sklearn.externals import joblib


from twitter_settings import *


class TopicListener(StreamListener):
    '''
    Overrides Tweepy class for Twitter Streaming API
    '''

    def __init__(self, model_path, vectorizer_path='vectorizer.pkl'):
        # load classifier
        self.clf = joblib.load(model_path)
        # tweet representation as tfidf
        self.vectorizer = joblib.load(vectorizer_path)
        # set up Twitter connection
        self.auth_handler = OAuthHandler(APP_KEY, APP_SECRET)
        self.auth_handler.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.api = API(self.auth_handler)

    def on_status(self, status):
        # ignore retweets
        if not hasattr(status,'retweeted_status') and status.in_reply_to_status_id == None:
            # preprocess
            tweet_text = status.text.encode('utf-8').replace('\n', '')
            # print (tweet_text)
            # classify
            tweet_vector = self.vectorizer.transform([tweet_text])
            job_tweet_prediction = self.clf.predict_proba(tweet_vector)[0,1]
            if job_tweet_prediction > 0.73:
                print tweet_text
                print job_tweet_prediction
                # retweet
                self.api.update_status(status='https://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))

    def on_error(self, status_code):
      print (status_code, 'error code')


def detect_jobs(model_path='random_forest.pkl'):
    '''
    Connect to Twitter API and fetch relevant tweets from the stream
    '''
    listener = TopicListener(model_path)

    # start streaming
    while True:
        try:
            stream = Stream(listener.auth_handler, listener)
            print ('Listening...')
            stream.sample(languages=['en'])
            # stream.sample()
        except Exception as e:
            # reconnect on exceptions
            print (e)
            continue


if __name__ == '__main__':
    detect_jobs()
