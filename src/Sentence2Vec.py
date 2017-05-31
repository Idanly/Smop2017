import os
import sys

from gensim import corpora, models

if os.path.exists("questions_dict.dict") and os.path.exists("questions_corpus.mm"):
    dictionary = corpora.Dictionary.load('questions_dict.dict')
    corpus = corpora.MmCorpus('questions_corpus.mm')
    print("Used files generated from first tutorial")
else:
    print("Please run first tutorial to generate data set")
    sys.exit(1)

tfidf = models.TfidfModel(corpus)

some_q = "where did pooh bear live"

some_q_vec = dictionary.doc2bow(some_q.lower().split())
print(tfidf[some_q_vec])
