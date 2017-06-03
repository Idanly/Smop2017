from pprint import pprint

from gensim import corpora, models
from nltk.corpus import stopwords
from six import iteritems

english_stopwords = set(stopwords.words('english'))
question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether',
                  'whence', 'whither', 'whatsoever'}
stopwords_with_questions = english_stopwords - question_words


def create_dictionary(sent_gen):
    dictionary = corpora.Dictionary(sent.lower().split() for sent in sent_gen)
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords_with_questions
                if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
    dictionary.compactify()  # remove gaps in id sequence after words that were removed
    return dictionary


sent_gen = (line for line in open('Texts\questions_unified.txt'))
dictionary = create_dictionary(sent_gen)
dictionary.save('questions_dict.dict')
print("created dictionary")


def create_corpus_gen():
    return (dictionary.doc2bow(line.lower().split()) for line in open('Texts\questions_unified.txt'))


model_tfidf = models.TfidfModel(create_corpus_gen())
print("created tfidf model")
corpus_tfidf = model_tfidf[create_corpus_gen()]
print("created tfidf of corpus")
lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)  # May be subject to change
print("created lsi model")

lsi_model.save('lsi_model.lsi')
pprint(lsi_model.show_topics(num_topics=10))
