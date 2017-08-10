#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Aug 9, 2017
.. codeauthor: svitlana vakulenko
<svitlana.vakulenko@gmail.com>

Classifies tweets in real time
'''
from collections import deque
from threading import Thread

from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

from twython import Twython

from twitter_settings import *
from stream import stream_tweets


class JobTweetsClassifier():

    def __init__(self, model_path, vectorizer_path='vectorizer.pkl'):
        # load classifier
        self.clf = joblib.load(model_path)
        # tweet representation as tfidf
        self.vectorizer = joblib.load(vectorizer_path)
        # connect to Twitter
        # twitter = Twython(APP_KEY, APP_SECRET)
        self.twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def launch(self):
        # start streaming tweets
        tweet_queue = deque()
        tweet_stream = Thread(target=stream_tweets, args=(tweet_queue,))
        tweet_stream.start()
        self.detect_jobs(tweet_queue, limit=1000)

    def detect_jobs(self, tweets_queue, limit):
        # save tweet_texts
        documents = []
        while True:
            if len(tweets_queue) > 0:
                tweet = tweets_queue.popleft()

                # ignore retweets
                if not 'retweeted_status' in tweet.keys() and tweet['in_reply_to_status_id'] == None:
                    tweet_text = tweet['text'].encode('utf-8').replace('\n', '')
                    # print (tweet_text)
                    tweet_vector = self.vectorizer.transform([tweet_text])
                    job_tweet_prediction = self.clf.predict_proba(tweet_vector)[0,1]
                    if job_tweet_prediction > 0.73:
                        print tweet_text
                        print job_tweet_prediction
                        # retweet
                        self.twitter.update_status(status='https://twitter.com/%s/status/%s' % (tweet['user']['screen_name'], tweet['id']))


def test_detect_jobs(model_path='random_forest.pkl'):
    jobs_monitor = JobTweetsClassifier(model_path)
    jobs_monitor.launch()


if __name__ == "__main__":
    test_detect_jobs()
