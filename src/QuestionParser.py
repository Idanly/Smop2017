from nltk import sent_tokenize


def extract_entities(text):
    entities = []
    for sentence in sent_tokenize(text):
        print(sentence)
        # chunks = ne_chunk(pos_tag(word_tokenize(sentence)))


if __name__ == '__main__':
    text = "This inland sea is bordered on the north by Europe, the east by Asia, and in the south by Africa. This 969,100 sq. mile body of water is approximately 2,300 miles in length, and has a maximum depth of 16,896 ft.\n"
    print(extract_entities(text))
