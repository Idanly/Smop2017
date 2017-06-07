import multiprocessing
from gensim import models

from SentenceScrapper import find_answer
from classifyQuestions import classifyQuestions
from decisionTree import decisionTree

if __name__ == '__main__':
    multiprocessing.freeze_support()
    import warnings

    warnings.simplefilter("ignore", UserWarning)
    warnings.simplefilter("ignore", DeprecationWarning)
    print("Loading w2v model...")
    word2vec_model = models.KeyedVectors.load_word2vec_format('Ignore\word2vec_6B.100d.w2v',
                                                              binary=False)
    print("Finished loading")
    while True:
        my_inp = input('enter your question: ')
        if my_inp == -1:
            break

        quest = classifyQuestions()
        vec = quest.createQuestionVector(my_inp)
        tree = decisionTree()
        expectedClass = tree.getClass(vec)
        opt_answers = find_answer(my_inp, word2vec_model)
        opt_answers.sort(key=lambda tup: tup[1], reverse=True)
        # print("Relevant sentences ordered:")
        # for sent in opt_answers:
        #     print(sent)

        fitSentences = []
        for (sentence, sim) in opt_answers:
            words = sentence.split()
            for word in words:
                if expectedClass == [5] or expectedClass == [11]:
                    if word.isdigit():
                        fitSentences.append(sentence)
                        break
                else:
                    if (quest.getHypernym(word, sentence) == expectedClass):
                        fitSentences.append(sentence)
                        break
        print("5 Fitting sentences ordered by relevance:")
        i = 0
        for sent in fitSentences:
            print(sent)
            i += 1
            if i >= 5:
                break
