from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.stem.snowball import SnowballStemmer
import inflection


class classifyQuestions:
    def __init__(self):
        self.flag = False

    def createQuestionVector(self, question):
        numOfFields = 15
        words = question.split(" ")
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
                if word == 'How' and words[1] == 'much':
                    vector[0] = 7
                elif word == 'How' and words[1] == 'many':
                    vector[0] = 8
                else:
                    vector[0] = question_words.index(word)
            elif word != 'much' or word != 'many':
                index = self.getHypernym(word, question)
                if index != None:
                    if self.flag == False:
                        vector[index] = vector[index] + 2
                        self.flag = True
                    else:
                        vector[index] = vector[index] + 1
        return vector

    def getHypernym(self, word_to_find, question):
        stopWords = set(stopwords.words('english'))
        if word_to_find in stopWords or word_to_find == 'was' or word_to_find == 'were':
            return None
        text = question.split()
        index = text.index(word_to_find)
        temp = pos_tag(text)
        if temp[index][1] == 'VBP' or temp[index][1] == 'VBD' or temp[index][1] == 'VBZ' or temp[index][1] == 'VBN' or \
                        temp[index][1] == 'VBG':
            return 10
        if word_to_find == 'human' or word_to_find == 'humans' or word_to_find == 'people':
            return 2
        categories = {1: wn.synset('animal.n.01'), 2: wn.synset('person.n.01'),
                      3: wn.synset('country.n.02'), 4: wn.synset('city.n.01'), 5: wn.synset('year.n.01'),
                      6: wn.synset('month.n.01'), 7: wn.synset('day.n.01'),
                      8: wn.synset('body_part.n.01'), 9: wn.synset('language.n.01'), 10: wn.synset('action.n.01'),
                      11: wn.synset('number.n.01'), 12: wn.synset('product.n.02'), 13: wn.synset('organization.n.01'),
                      14: wn.synset('event.n.01')}
        question_words = ['What', 'Why', 'How', 'Where', 'When', 'Who', 'How much', 'How many', 'Which']
        if word_to_find in question_words:
            return None
        stemmer = SnowballStemmer("english")
        try:
            if word_to_find == 'country' or word_to_find == 'product' or word_to_find == 'chicken' or word_to_find == 'cost':
                word = wn.synset(word_to_find + '.n.2')
            else:
                word = wn.synset(
                    word_to_find + '.n.1')  # we assume it is the first definition because we cant do it better
        except:
            try:
                word_to_find = inflection.singularize(word_to_find)
                if word_to_find == 'country' or word_to_find == 'product' or word_to_find == 'chicken' or word_to_find == 'cost':
                    word = wn.synset(word_to_find + '.n.2')
                else:
                    word = wn.synset(
                        word_to_find + '.n.1')  # we assume it is the first definition because we cant do it better
            except:
                return None
        root = word.root_hypernyms()
        while (word != root[0]):
            if word == wn.synset('quantity.n.01') or word == wn.synset('measure.n.02') or word == wn.synset(
                    'magnitude.n.01') or word == wn.synset('age.n.01') or (word == wn.synset(
                'time.n.05') and index == 1) or word == wn.synset('proportion.n.01') or word == wn.synset('quality.n.01'):
                return 11
            if word == wn.synset('art.n.01'):
                return 12
            if word == wn.synset('weekday.n.01'):
                return 7
            if word == wn.synset('body.n.01'):
                return 8
            if word == wn.synset('capital.n.03'):
                return 4
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
    question = QuestToClassify("What day comes after thursday")
    print(question.createQuestionVector())
