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
    return (dictionary.doc2bow(line.lower().split()) for line in open('wikipedia-crawler-master\philosophy.txt'))


model_tfidf = models.TfidfModel(create_corpus_gen())
print("created tfidf model")
corpus_tfidf = model_tfidf[create_corpus_gen()]
print("created tfidf of corpus")

pprint(lsi_model.show_topics(num_topics=10))
lsi_model.add_documents(corpus_tfidf)
print("added documents to lsi model")
pprint(lsi_model.show_topics(num_topics=10))

lsi_model.save('lsi_model.lsi')
