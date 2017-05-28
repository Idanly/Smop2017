from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


class QuestToClassify:
    # numOfFields = 0

    def __init__(self, question):
        self.q_word = question[0]
        self.query_vec = question[1:len(question)]

    def createQuestionVector(self):
        numOfFields = 14
        words = self.query_vec().split()
        vector = []
        question_words = ['what', 'why', 'how', 'how much', 'how many' 'where', 'when', 'who', 'which']
        for i in range(numOfFields):
            vector.append(0)
        for word in words:
            if words in question_words and vector[0] == 0:
                vector[0] = question_words.index(word)
            else:
                index = word.getHypernym()
                if index != None:
                    vector[index] = + 1
        return vector

    def getHypernym(word_to_find, vector):
        categories = {1: wn.synset('animal.n.01'), 2: wn.synset('color.n.01'),
                      3: wn.synset('country.n.01'), 4: wn.synset('city.n.01'), 5: wn.synset('year.n.01'),
                      6: wn.synset('month.n.01'), 7: wn.synset('day.n.01'),
                      8: wn.synset('body.n.01'), 9: wn.synset('language.n.01'), 10: wn.synset('action.n.01'),
                      11: wn.synset('person.n.01'), 12: wn.synset('number.n.01'), 13: wn.synset('place.n.01')}
        stopWords = set(stopwords.words('english'))
        if word_to_find in stopWords:
            return None
        question_words = ['what', 'why', 'how', 'where', 'when', 'who']
        if word_to_find in question_words:
            return None
        word = wn.synset(word_to_find + '.n.1')  # we assume it is the first definition because we cant do it better
        root = word.root_hypernyms()
        while (word != root):
            if word in categories:
                return (list(categories.keys())[list(categories.values()).index(word)])
        if root in categories:
            return (list(categories.keys())[list(categories.values()).index(root)])
        return None
