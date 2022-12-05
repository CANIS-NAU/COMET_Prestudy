import pandas as pd
import os

print('creating empty dataframe...')
samples = pd.DataFrame()

print('getting files...')
files = os.listdir('.')

print('filtering files...')
files = [file for file in files if '.tsv' in file and 'reddit' in file]

for file in files:
    try:
        print('getting ' + file + '...')
        sample = 100

        papers = pd.read_csv(file, sep='\t')

        print('sampling data...')
        papers = papers.dropna(subset=['text'])
        papers = papers.drop_duplicates()
        num_posts = len(papers)
        if num_posts < 100:
            sample = num_posts
        papers = papers['text'].sample(sample)

        print('adding to pot...')
        samples = pd.concat([samples, papers])
    except:
        continue

sample = 100
if len(samples) < sample:
    sample = len(samples)

print('getting final sample...')
final = samples.sample(sample)

print('creating csv...')
final.to_csv('topic_analysis.csv')

print('all done!')
