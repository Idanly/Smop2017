from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


# I need to find the problem with names and two words
from nltk.corpus.reader import WordNetError


def getHypernym(word_to_find):
    categories = {0: wn.synset('person.n.01'), 1: wn.synset('animal.n.01'), 2: wn.synset('color.n.01'),
                  3: wn.synset('country.n.01'), 4: wn.synset('city.n.01'), 5: wn.synset('year.n.01'),
                  6: wn.synset('month.n.01'), 7: wn.synset('weekday.n.01'),  # find the problem with calender day
                  8: wn.synset('body.n.01'), 9: wn.synset('language.n.01'),
                  10: wn.synset('action.n.01'), 11: wn.synset('number.n.01')}  # fix body to body part
    stopWords = set(stopwords.words('english'))
    if word_to_find in stopWords:
        return None
    """try:"""
    word = wn.synset(word_to_find + 'n.1')  # we assume it is the first definition because we cant do it better
    root = word.root_hypernyms()[0]
    while (word != root):
        print('a')
        if word in categories.values():
            return (list(categories.keys())[list(categories.values()).index(word)])
        word = word.hypernyms()[0]
    if root in categories:
        return (list(categories.keys())[list(categories.values()).index(root)])
    return None


a = 'What was the number of member nations of the U.N. in 2000?'
words = a.split()
vector = []
question_words = ['What', 'Why', 'How', 'How much', 'How many' 'Where', 'When', 'Who', 'Which']
for i in range(14):
    vector.append(0)
for word in words:
    if word in question_words and vector[0] == 0:
        vector[0] = question_words.index(word) + 1
    else:
        index = getHypernym(word)
        if index != None:
            vector[index] = + 1
print(vector)
