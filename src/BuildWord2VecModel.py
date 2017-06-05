from gensim import corpora, models
from nltk.corpus import stopwords
from six import iteritems

english_stopwords = set(stopwords.words('english'))
question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether',
                  'whence', 'whither', 'whatsoever'}
stopwords_with_questions = english_stopwords - question_words

# load id->word mapping (the dictionary), one of the results of step 2 above
id2word = corpora.Dictionary.load_from_text('D:/Documents/wiki_dump/_wordids.txt.bz2')
print(id2word)
# load corpus iterator
tfidf_model = models.TfidfModel.load('D:/Documents/wiki_dump/_tfidf.tfidf_model')
print(tfidf_model)
mm = corpora.MmCorpus('D:/Documents/wiki_dump/_bow.mm')
print(mm)

corpus_tfidf = tfidf_model[mm]
print("created corpus tfidf wrapper")

word2vec_model = models.Word2Vec(mm)
print(word2vec_model)
print(word2vec_model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
print(word2vec_model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
print(word2vec_model.wv.similarity('woman', 'man'))
word2vec_model.save('wiki_word2vec.w2v')
print("saved model")
