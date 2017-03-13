# -*- coding:utf-8 -*-
"""
Created on the 10/03/2017
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import argparse
import heapq
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


biggest_businesses = [
    'Starbucks', 'Hash House A Go Go', "McDonald's",
    'Chipotle Mexican Grill', 'Mon Ami Gabi', 'Bacchanal Buffet',
    'Wicked Spoon', 'Gordon Ramsay BurGR', 'Earl of Sandwich',
    'Buffalo Wild Wings'
]
biggest_businesses = ', '.join(biggest_businesses)


# Parse program options first
desc = 'Find business strengths and weaknesses.'
parser = argparse.ArgumentParser(description=desc)
parser.add_argument('name', metavar='name', type=str, nargs='+',
                    help='business name (e.g. '+ biggest_businesses + ')')
args = parser.parse_args()
biz_name = ' '.join(args.name)

print('Loading datasets ...')
biz = pd.read_csv('data/yelp_academic_dataset_business.csv')[['business_id', 
                                                              'name']]
biz = biz[biz['name'] == biz_name]

if len(biz) == 0:
    raise ValueError('Business name was not found, try one of these:' + \
                     biggest_businesses)

reviews = pd.read_csv('data/yelp_academic_dataset_review.csv')
mask = reviews['business_id'].isin(biz['business_id'])
biz_reviews = reviews[mask][['text', 'stars']]

print("Number of reviews found: {}".format(biz_reviews.shape[0]))

tfidf = TfidfVectorizer(stop_words='english', max_features=300, 
                        ngram_range=(1, 3))
model = LinearRegression() 

corpus = biz_reviews['text'].values
X = tfidf.fit_transform(corpus)
y = biz_reviews['stars'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

model.fit(X_train, y_train)
print('Train R^2: {:.1f} %'.format(100*model.score(X_train, y_train)))
print('Test R^2: {:.1f} %'.format(100*model.score(X_test, y_test)))
model.fit(X, y)


# Get the 10 highest and the 10 lowest weights indices 
max_indices = heapq.nlargest(10, range(len(model.coef_)), key=model.coef_.__getitem__)
min_indices = heapq.nsmallest(10, range(len(model.coef_)), key=model.coef_.__getitem__)

def print_summary(indices):
    features = tfidf.get_feature_names()
    for i in indices:
        feat = features[i]
        print('{} ({}): {:.2f}'.format(feat, tfidf.vocabulary_[feat], model.coef_[i]))

print('Business summary: ' + biz_name + '\n')
print_summary(max_indices)
print('----------')
print_summary(reversed(min_indices))
