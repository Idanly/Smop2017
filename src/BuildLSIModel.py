from pprint import pprint

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

lsi_model = models.LsiModel(mm, id2word=id2word, num_topics=100)  # May be subject to change
print("created lsi model")
lsi_model.save('lsi_model.lsi')
pprint(lsi_model.show_topics(num_topics=10))

corpus_lsi = lsi_model[corpus_tfidf]
corpora.MmCorpus.serialize('corpus_lsi.mm', corpus_lsi)

