from gensim import corpora, models, matutils


class RelevantSentencesScrapper:
    def __init__(self, s_scrapper, search_words, max_sentences=-1):
        self.search_words = search_words
        self.max_sentences = max_sentences
        self.sentences_returned = 0
        self.s_iter = s_scrapper.__iter__()
        self.returned_sentences = list()
        self.lsi_model = models.LsiModel.load('lsi_model.lsi')
        self.dictionary = corpora.Dictionary.load('questions_dict.dict')
        self.similarity_hi_thresh = 1
        self.similarity_low_thresh = 0.4

    def __iter__(self):
        while self.sentences_returned != self.max_sentences:
            try:
                next_sentence = next(self.s_iter)
                if self.is_sentence_relevant(self.search_words, next_sentence):
                    self.sentences_returned += 1
                    self.returned_sentences.append(next_sentence)
                    yield next_sentence
            except StopIteration:
                break

    def is_sentence_relevant(self, words, sentence):
        query_vec = self.dictionary.doc2bow(word.lower() for word in words)
        query_lsi = self.lsi_model[query_vec]
        sentence_vec = self.dictionary.doc2bow(sentence.lower().split())
        sentence_lsi = self.lsi_model[sentence_vec]
        similarity = self.cosine_similarity(query_lsi, sentence_lsi)

        return self.similarity_hi_thresh > similarity > self.similarity_low_thresh

    def cosine_similarity(self, first_lsi, second_lsi):
        return matutils.cossim(first_lsi, second_lsi)

    def get_returned_sentences(self):
        return self.returned_sentences
