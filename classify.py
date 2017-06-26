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


# 1. Load the labeled dataset into a dataframe
def load_dataset(dataset_path):
    return pd.read_csv(dataset_path, sep='\t',header=None)


def test_load_dataset():
    dataset_path = 'data/my_tweets.csv'
    df = load_dataset(dataset_path)
    assert df.shape
    print "Loaded table", df.shape
    print df[0]


def convert_dataset(dataset_path, output_path):
    '''
    dataset formatting for fastText classification
    + remove paragraphs with line separators: save one tweet per line
    + balance classes
    + shuffle samples
    '''
    df = load_dataset(dataset_path)
    df[0] = df[0].str.replace('\n', '')
    print "Loaded table", df.shape
    # with open(output_path, 'w') as f_out:
    #     for row in df.rows():
    #         f_out.write(row)
    # show class distribution
    # print df.groupby(1).count()
    false_samples = df.loc[df[1]==False]
    true_samples = df.loc[df[1]==True]
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
    dataset.to_csv(output_path, sep=',', index=False, header=False, columns=[1,0])


def test_convert_dataset():
    dataset_path = 'data/my_tweets.csv'
    output_path = 'data/my_tweets_ft.csv'
    convert_dataset(dataset_path, output_path)


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
    test_convert_dataset()