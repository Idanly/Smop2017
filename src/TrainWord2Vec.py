import multiprocessing

import SentenceScrapper


def main():
    for question in (line for line in open('Texts/questions_unified.txt')):
        print("Asking question: " + question)
        SentenceScrapper.find_answer(question)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
