#!/usr/bin/env python3
import argparse
import pathlib
import sys
from ast import literal_eval

import pandas as pd

"""Script that takes a single csv file and returns the collected hashtag counts as a csv.
Output is sent to stdout for easy piping into files.
"""

def extract_hashtags(file: str):
    data = pd.read_csv(file, low_memory=False, encoding='utf-8', encoding_errors=None)['entities.hashtags'].dropna('index')
    data = [literal_eval(line) for line in data]
    for post in data:
        for dictionary in post:
            yield dictionary['tag']

def count_hashtags(post_hashtags):
    pd.Series(post_hashtags).value_counts().to_csv(sys.stdout)
    

parser = argparse.ArgumentParser()
parser.add_argument('filepath', help='path to twitter data csv')
args = parser.parse_args()
path = pathlib.Path(args.filepath)

if not path.is_file():
    sys.stderr.write("[Error] - File not found")
    exit(1)
else:
    tags = list(extract_hashtags(path.resolve()))
    count_hashtags(tags)
