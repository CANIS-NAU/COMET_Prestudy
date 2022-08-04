from distutils.log import error
import pandas as pd
import os

relevant = pd.DataFrame()
files = os.listdir()
files = [file for file in files if 'filtered_reddit_posts.tsv' in file]

for file in files:
    papers = pd.read_csv(file, sep='\t')
    papers = papers[papers['post_id'].str.contains('_') == False]
    
    relevant = pd.concat([papers, relevant])

print(len(relevant))