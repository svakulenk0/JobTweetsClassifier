#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jun 27, 2017
.. codeauthor: svitlana vakulenko
<svitlana.vakulenko@gmail.com>

Collects tweets harvesting the official Twitter API
'''

from collections import deque

from threading import Thread
from requests.exceptions import ChunkedEncodingError

from twython import TwythonStreamer
from twitter_settings import *


class TwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, token, token_secret, tqueue):
        self.tweet_queue = tqueue
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, token, token_secret)

    def on_success(self, data):
        if 'text' in data:
            self.tweet_queue.append(data)

    def on_error(self, status_code, data):
        print status_code


def stream_tweets(tweets_queue):
    try:
        stream = TwitterStream(APP_KEY, APP_SECRET,
                               OAUTH_TOKEN, OAUTH_TOKEN_SECRET, tweets_queue)
        # You can filter on keywords, or simply draw from the sample stream
        # stream.statuses.filter(track='twitter', language='en')
        stream.statuses.sample(language='en')
    except ChunkedEncodingError:
        # Sometimes the API sends back one byte less than expected which results in an exception in the
        # current version of the requests library
        stream_tweets(tweets_queue)


def process_tweets(tweets_queue, limit):
    # save tweet_texts
    documents = []
    while True:
        if len(tweets_queue) > 0:
            tweet = tweets_queue.popleft()
            tweet_text = tweet['text'].encode('utf-8').replace('\n', '')
            print tweet_text


def test_stream_tweets():
    tweet_queue = deque()
    tweet_stream = Thread(target=stream_tweets, args=(tweet_queue,))
    tweet_stream.start()

    process_tweets(tweet_queue, limit=1000)


if __name__ == "__main__":
    test_stream_tweets()
