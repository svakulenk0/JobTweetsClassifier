#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jan 5, 2017
.. codeauthor: svitlana vakulenko
<svitlana.vakulenko@gmail.com>

Identifies the tweets containing a job ad
'''

# Load text processing libraries
import pandas as pd

import fasttext


DATASET_PATH = 'data/all_tweets.csv'
DATASET_PATH_FT_FORMAT = 'data/all_tweets_ft.csv'
TEST_DATASET_PATH = 'data/test_tweets_ft.csv'


# 1. Load the labeled dataset into a dataframe
def load_dataset(dataset_path):
    return pd.read_csv(dataset_path, sep='\t',header=None)


def test_load_dataset():
    dataset_path = 'data/my_tweets.csv'
    df = load_dataset(dataset_path)
    assert df.shape
    print "Loaded table", df.shape
    print df[0]


def prepare_dataset(dataset_path, output_path):
    '''
    dataset formatting for fastText classification
    + remove paragraphs with line separators: save one tweet per line
    + balance classes
    + shuffle samples
    '''
    df = load_dataset(dataset_path)
    
    # preprocessing:
    # strip new line chars
    df[1] = df[1].str.replace('\n', '')
    # lowercase
    df[1] = df[1].str.lower()
    # df[0] = str(df[0]).lower()
    df[0] = '__label__' + df[0].astype(str)

    print "Loaded table", df.shape
    # with open(output_path, 'w') as f_out:
    #     for row in df.rows():
    #         f_out.write(row)
    # show class distribution
    # print df.groupby(1).count()
    false_samples = df.loc[df[0]=='__label__False']
    true_samples = df.loc[df[0]=='__label__True']
    print len(false_samples), len(true_samples)
    # downsample false classes
    n_samples_per_class = min(len(false_samples), len(true_samples))
    false_samples = false_samples.sample(n=n_samples_per_class)
    true_samples = true_samples.sample(n=n_samples_per_class)
    print len(false_samples), len(true_samples)
    dataset = true_samples.append(false_samples, ignore_index=True)
    # shuffle
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    print len(dataset)
    dataset.to_csv(output_path, sep=',', index=False, header=False)


def test_prepare_dataset(dataset_path=DATASET_PATH, output_path=DATASET_PATH_FT_FORMAT):
    prepare_dataset(dataset_path, output_path)


def train_fasttext(dataset_path=DATASET_PATH_FT_FORMAT):
    # training
    # ./fasttext supervised -input data.train.txt -output model
    classifier = fasttext.supervised(dataset_path, 'model', epoch=50)
    classifier.word_ngrams = 5
    evaluate_classifier(classifier)


def evaluate_classifier(classifier):
    # evaluation
    # ./fasttext test model.bin test.txt
    result = classifier.test(TEST_DATASET_PATH)
    print 'P@1:', result.precision
    print 'R@1:', result.recall
    print 'Number of examples:', result.nexamples


def explain_classifier():
    # load model
    classifier = fasttext.load_model('model.bin', encoding='utf-8')
    # evaluation
    evaluate_classifier(classifier)


# def preprocess(tweets):
#     '''
#     Procedure to preprocess a list of tweet texts
    
#     tweets - list of strings

#     '''


# def test_preprocess():
#     tweets = ["""RT @fchollet: How I get my ML news: 

# 1) Twitter 
# 2) arxiv
# 3) mailing lists 
# .
# .
# .
# 97) overheard at ramen place
# 98) graffiti in bathroom st…"""]
#     preprocess(tweets)


if __name__ == '__main__':
    # test_prepare_dataset()
    # train_fasttext()
    explain_classifier()