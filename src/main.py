import multiprocessing
from classifyQuestions import classifyQuestions
from decisionTree import decisionTree
from SentenceScrapper import find_answer

if __name__ == '__main__':
    multiprocessing.freeze_support()
    my_inp = input('enter your question: ')
    quest = classifyQuestions()
    vec = quest.createQuestionVector(my_inp)
    tree = decisionTree()
    expectedClass = tree.getClass(vec)
    opt_answers = find_answer(my_inp)
    opt_answers.sort(key=lambda tup: tup[1], reverse=True)
    print("Relevant sentences ordered:")
    for sent in opt_answers:
        print(sent)

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
    print(fitSentences)

