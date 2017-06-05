from pprint import pprint

from gensim import corpora, models
from nltk.corpus import stopwords

lsi_model = models.LsiModel.load('lsi_model.lsi')
dictionary = corpora.Dictionary.load('questions_dict.dict')

english_stopwords = set(stopwords.words('english'))
question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether',
                  'whence', 'whither', 'whatsoever'}
stopwords_with_questions = english_stopwords - question_words


def create_corpus_gen():
    return corpora.MmCorpus('questions_corpus.mm')

question_corpus = create_corpus_gen()
model_tfidf = models.TfidfModel(question_corpus)
print("created tfidf model")
corpus_tfidf = model_tfidf[question_corpus]
print("created tfidf of corpus")

pprint(lsi_model.show_topics(num_topics=10))
lsi_model.add_documents(corpus_tfidf, decay=0.6)
print("added documents to lsi model")
pprint(lsi_model.show_topics(num_topics=10))

# lsi_model.save('lsi_model.lsi')
