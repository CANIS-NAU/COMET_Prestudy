from distutils.log import error
import pandas as pd
import os

hashtags = {}

papers = pd.read_csv('filtered_reddit_posts.tsv', sep='\t')
papers = papers[papers['post_id'].str.contains('_') == False]
papers = papers[papers['text'].str.contains('#')]
papers = papers[papers['text'].str.contains('&#x200B;') == False]
papers = papers['text']

for paper in papers:
    paper = paper.split(' ')
    
    for element in paper:
        if '#' in element:
            element = element.split('#')
            
            for i in element:
                if i != '':
                    i = i.replace('\n', '')
                    if i not in hashtags:
                        hashtags[i] = 1
                    else:
                        hashtags[i] += 1

print(hashtags)
print(len(hashtags))