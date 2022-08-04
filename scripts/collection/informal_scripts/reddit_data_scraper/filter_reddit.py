import pandas as pd
import os

relevant = pd.DataFrame()
files = os.listdir()
files = [file for file in files if '.tsv' in file and 'reddit' in file]

for file in files:
    papers = pd.read_csv(file, sep='\t', lineterminator='\n')
    papers = papers.drop_duplicates()
    papers = papers.dropna(subset=['text'])
    papers = papers[papers['text'].str.contains('speedtest|speed test')]
    
    relevant = pd.concat([papers, relevant])

relevant.to_csv('filtered_reddit_posts.tsv', sep='\t')