## Set the path of where the csv files are located, as well as initial import statements
csv_data_path = "" # **PLACE CSV FILE HERE**
sep = "\t" # csv delimiter used
small_model = True # use smaller ML model for better performance, less accuracy

from pathlib import Path 
import pandas as pd
import numpy as np

# Gensim imports
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy
import spacy
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# visualization
import pyLDAvis
import pyLDAvis.gensim_models

## Functions to handle data loading and data writing
def load_data(filename) -> pd.DataFrame:
    filename = Path(filename)
    if not filename.is_file():
        raise FileNotFoundError

    with open(filename.resolve(), 'r', encoding='utf-8') as file:
        data = pd.read_csv(file, sep=sep)
    return data

def load_data_by_file(directory: Path) -> pd.DataFrame:
    for data_file in Path.glob(Path.joinpath(directory, '*.csv')):
            yield load_data(data_file.resolve())

def write_data(filename: Path, data: pd.DataFrame):
    with open(filename.as_uri(), 'w', encoding='utf-8') as f:
        data.to_csv(f, sep=sep)

# obtain the stop words
stopwords = stopwords.words("english")
stopwords

data = load_data(csv_data_path)['content']
data.head()

# Content Preprocessing
def lemmatize(posts: pd.DataFrame, allowed_post_tags=["NOUN", "ADJ", "VERB", "ADV"]):
    nlp = spacy.load("en_core_web_sm" if small_model else "en_core_web_trf", disable=["parser", 'ner'])
    texts_out = []

    for post in posts:
        doc = nlp(post)
        new_text = []
        for token in doc:
            if token.pos_ in allowed_post_tags:
                new_text.append(token.lemma_)
        final = ' '.join(new_text)
        texts_out.append(final)
    return texts_out

lemmatized_data = lemmatize(data.astype(str))
lemmatized_data[0][:10]

def tokenize_lemma(posts: list):
    final = []
    for post in posts:
        new = gensim.utils.simple_preprocess(post, deacc=True)
        final.append(new)
    return final

tokenized_data = tokenize_lemma(lemmatized_data)
tokenized_data[0][:10]

# # Generate id2word dictionary
id2word = corpora.Dictionary(tokenized_data)

corpus = []

for text in tokenized_data:
    new = id2word.doc2bow(text)
    corpus.append(new)

corpus[0][:10]

# LDA Visualization
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=30,
random_state=100, update_every=1, chunksize=100, passes=10, alpha="auto")

pyLDAvis.enable_notebook()
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word, mds='mmds', R=30)
vis


