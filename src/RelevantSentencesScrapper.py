import numpy as np
from gensim import models

from RelevancyFinder import important_words


class RelevantSentencesScrapper:
    def __init__(self, s_scrapper, search_words, model, max_sentences=-1):
        self.search_words = search_words
        self.max_sentences = max_sentences
        self.sentences_returned = 0
        self.s_iter = s_scrapper.__iter__()
        self.returned_sentences = list()
        """
        self.lsi_model = models.LsiModel.load('Ignore\lsi_model.lsi')
        self.dictionary = corpora.Dictionary.load_from_text('_wordids.txt.bz2')
        """
        # self.word2vec_model = models.KeyedVectors.load_word2vec_format('Ignore/GoogleNews-vectors-negative300.bin',
        #                                                               binary=True)

        # self.word2vec_model = models.KeyedVectors.load_word2vec_format('Ignore\word2vec_6B.100d.w2v',
        #                                                              binary=False)
        self.word2vec_model = model
        self.similarity_hi_thresh = 1
        self.similarity_low_thresh = 0.6

    def __iter__(self):
        while self.sentences_returned != self.max_sentences:
            try:
                next_sentence = next(self.s_iter)
                similarity = self.sentence_similarity(self.search_words, next_sentence)
                if self.similarity_hi_thresh > similarity > self.similarity_low_thresh:
                    self.sentences_returned += 1
                    self.returned_sentences.append((next_sentence, similarity))
                    yield (next_sentence, similarity)
            except StopIteration:
                break

    def sentence_similarity(self, words, sentence):
        query_vec = np.zeros((100,))
        for word in words:
            try:
                query_vec += self.word2vec_model[word]
            except KeyError:
                continue

        sentence_vec = np.zeros((100,))
        for word in important_words(sentence.lower()):
            try:
                sentence_vec += self.word2vec_model[word]
            except KeyError:
                # print("word: " + word + " not in model")
                continue
        """
        query_lsi = self.lsi_model[query_vec]
        sentence_vec = self.dictionary.doc2bow(sentence.lower().split())
        sentence_lsi = self.lsi_model[sentence_vec]
        """
        similarity = RelevantSentencesScrapper.cosine_similarity(query_vec, sentence_vec)
        return similarity

    @staticmethod
    def cosine_similarity(first_np_vec, second_np_vec):
        try:
            result = np.dot(np.asarray(first_np_vec), np.asarray(second_np_vec)) / \
                     (np.linalg.norm(first_np_vec) * np.linalg.norm(second_np_vec))
            return float(result)
        except RuntimeWarning:
            return 0

    def get_returned_sentences(self):
        return self.returned_sentences
