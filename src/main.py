import multiprocessing
from classifyQuestions import classifyQuestions
from decisionTree import decisionTree
from SentenceScrapper import find_answer

if __name__ == '__main__':
    multiprocessing.freeze_support()
    input = input('enter your question: ')
    quest = classifyQuestions()
    vec = quest.createQuestionVector(input)
    tree = decisionTree()
    expectedClass = tree.getClass(vec)
    opt_answers = find_answer(input)
    fitSentences = []
    for sentence in opt_answers:
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

