#!/usr/bin/env python3

# Using scikit-learn to label mlab sample data

import numpy as np
import pandas as pd 
import re
from nltk.corpus import stopwords
stop_words=set(stopwords.words('english'))
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# number of posts in each category

# how many posts have multi labels

# distribution of the number of words in post texts

# number of missing post text

## Data processing

# text scrubbing

# Split data for training

## Classifiers training

