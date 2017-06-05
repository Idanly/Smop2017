from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.snowball import SnowballStemmer


class QuestToClassify:
    # numOfFields = 0

    def __init__(self, question):
        self.quest = question
        self.flag = False

    def createQuestionVector(self):
        numOfFields = 15
        words = self.quest.split(" ")
        vector = []
        question_words = ['jhjh', 'What', 'Why', 'How', 'Where', 'When', 'Who', 'How much', 'How many', 'Which']
        if words[0] == 'What' or words[0] == 'How' or words[0] == 'Which':
            self.flag = False
        else:
            self.flag = True
        for i in range(numOfFields):
            vector.append(0)
        for word in words:
            if word in question_words and vector[0] == 0:
                vector[0] = question_words.index(word)
            else:
                index = self.getHypernym(word)
                if index != None:
                    if self.flag == False:
                        vector[index] = + 2
                        self.flag = True
                    else:
                        vector[index] = + 1
        return vector

    def getHypernym(self, word_to_find):
        text = self.quest.split()
        index = text.index(word_to_find)
        temp = pos_tag(text)
        if temp[index][1] == 'VBP' or temp[index][1] == 'VBD' or temp[index][1] == 'VBZ' or temp[index][1] == 'VBN' or \
                        temp[index][1] == 'VBG':
            return 10
        categories = {1: wn.synset('animal.n.01'), 2: wn.synset('person.n.01'),
                      3: wn.synset('country.n.02'), 4: wn.synset('city.n.01'), 5: wn.synset('year.n.01'),
                      6: wn.synset('month.n.01'), 7: wn.synset('day.n.01'),
                      8: wn.synset('body_part.n.01'), 9: wn.synset('language.n.01'), 10: wn.synset('action.n.01'),
                      11: wn.synset('number.n.01'), 12: wn.synset('show.n.01'), 13: wn.synset('organization.n.01'),
                      14: wn.synset('event.n.01')}
        stopWords = set(stopwords.words('english'))
        if word_to_find in stopWords:
            return None
        question_words = ['What', 'Why', 'How', 'Where', 'When', 'Who', 'How much', 'How many', 'Which']
        if word_to_find in question_words:
            return None
        stemmer = SnowballStemmer("english")
        try:
            word = wn.synset(word_to_find + '.n.1')  # we assume it is the first definition because we cant do it better
        except:
            word_to_find = stemmer.stem(word_to_find)
            word = wn.synset(word_to_find + '.n.1')
        root = word.root_hypernyms()
        while (word != root[0]):
            if word == wn.synset('quantity.n.01') or word == wn.synset('measure.n.02') or word == wn.synset(
                    'magnitude.n.01') or word == wn.synset('age.n.01'):
                return 11
            if word.instance_hypernyms() != []:
                word = word.instance_hypernyms()[0]
            elif word.instance_hypernyms() == [] and word.hypernyms() == []:
                return None
            if word in categories.values():
                return (list(categories.keys())[list(categories.values()).index(word)])
            word = word.hypernyms()[0]
        if root[0] in categories.values():
            return (list(categories.keys())[list(categories.values()).index(root)])
        return None


if __name__ == "__main__":
    question = QuestToClassify("When did mozart get his first piano")
    print(question.createQuestionVector())
