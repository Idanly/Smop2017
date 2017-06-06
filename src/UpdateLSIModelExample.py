from pprint import pprint
from gensim import corpora, models

lsi_model = models.LsiModel.load('Ignore\lsi_model.lsi')
dictionary = corpora.Dictionary.load('questions_dict.dict')


def create_corpus_gen():
    for line in open('Texts\questions_unified.txt'):
        # assume there's one document per line, tokens separated by whitespace
        yield dictionary.doc2bow(line.lower().split())

question_corpus = create_corpus_gen()
model_tfidf = models.TfidfModel(question_corpus)
print("created tfidf model")
corpus_tfidf = model_tfidf[question_corpus]
print("created tfidf of corpus")

pprint(lsi_model.show_topics(num_topics=10))
lsi_model.add_documents(corpus_tfidf, decay=0.9)
print("added documents to lsi model")
pprint(lsi_model.show_topics(num_topics=10))

lsi_model.save('Ignore\lsi_model.lsi')
