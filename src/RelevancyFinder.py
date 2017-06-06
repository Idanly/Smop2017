from nltk.corpus import stopwords

english_stopwords = set(stopwords.words('english'))
question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether',
                  'whence', 'whither', 'whatsoever'}
stopwords_with_questions = english_stopwords - question_words


def important_query_words(query):
    return [word for word in query.split() if word not in stopwords_with_questions]


def important_words(sentence):
    return [word for word in sentence.split() if word not in english_stopwords]
