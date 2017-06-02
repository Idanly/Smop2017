class RelevantSentencesScrapper:
    def __init__(self, s_scrapper, search_words, max_sentences=-1):
        self.search_words = search_words
        self.max_sentences = max_sentences
        self.sentences_returned = 0
        self.s_iter = s_scrapper.__iter__()
        self.returned_sentences = list()

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
        # Empty sentences are not good
        if len(sentence) == 0:
            return False
        # Sentences that are contained in the query aren't good either
        if all(word in words for word in sentence.split()):
            return False
        percentage_to_be_relevant = 0.4  # we need to find the optimal percentage
        counter = 0.0
        for word in words:
            if word in sentence:
                counter += 1
        if counter / len(words) >= percentage_to_be_relevant:
            return True

    def get_returned_sentences(self):
        return self.returned_sentences
