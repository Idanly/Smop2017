from gensim import corpora, models
from nltk.corpus import reuters
from six import iteritems


"""
# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = corpora.Dictionary.load('questions_dict.dict')
print(id2word)
# load corpus iterator
tfidf_model = models.TfidfModel.load('D:/Documents/wiki_dump/_tfidf.tfidf_model')
print(tfidf_model)
mm = corpora.MmCorpus('D:/Documents/wiki_dump/_bow.mm')
print(mm)
i = 0
for sent in mm:
    print(sent)
    i += 1
    if i > 1000:
        break

corpus_tfidf = tfidf_model[mm]
print("created corpus tfidf wrapper")
"""


def text8_gen():
    for line in open('text8'):
        return line.lower().split()

sentences = text8_gen()
word2vec_model = models.Word2Vec(sentences, size=100, window=5, min_count=5, workers=4)
word2vec_model.save('word2vec_model.w2v')
print("saved model")
print(word2vec_model)
print(word2vec_model.wv.most_similar(positive=['cat', 'wolf'], negative=['dog']))
print(word2vec_model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
print(word2vec_model.wv.similarity('woman', 'man'))

