from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from six import iteritems


class RelevancyFinder:
    def __init__(self):
        self.english_stopwords = set(stopwords.words('english'))
        self.question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether',
                               'whence', 'whither', 'whatsoever'}
        self.stopwords_with_questions = self.english_stopwords - self.question_words

    def important_query_words(self, query):
        return [word for word in query.split() if word not in self.stopwords_with_questions]

    def find_most_relevant_sentence(self, query, rel_sentences):
        dictionary = corpora.Dictionary(sent.lower().split() for sent in rel_sentences)
        stop_ids = [dictionary.token2id[stopword] for stopword in self.english_stopwords
                    if stopword in dictionary.token2id]
        once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
        dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
        dictionary.compactify()  # remove gaps in id sequence after words that were removed

        corpus_list = [dictionary.doc2bow(sent.lower().split()) for sent in rel_sentences]
        corpora.MmCorpus.serialize('results_corpus.mm', corpus_list)
        corpus = corpora.MmCorpus('results_corpus.mm')

        model_tfidf = models.TfidfModel(corpus)
        corpus_tfidf = model_tfidf[corpus]
        lsi_model = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=70)
        query_vec = dictionary.doc2bow(query.lower().split())
        query_lsi = lsi_model[query_vec]
        index = similarities.MatrixSimilarity(lsi_model[corpus])
        sims = index[query_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        rel_sentences_ordered = [rel_sentences[int(index)] for (index, sim) in sims]
        return rel_sentences_ordered
