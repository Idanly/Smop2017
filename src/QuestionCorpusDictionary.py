from gensim import corpora
from nltk.corpus import stopwords
from six import iteritems

english_stopwords = set(stopwords.words('english'))
question_words = {'what', 'why', 'how', 'where', 'when', 'who', 'which', 'whose', 'whom', 'whether', 'whence',
                  'whither', 'whatsoever'}
stoplist = english_stopwords - question_words

# collect statistics about all tokens
dictionary = corpora.Dictionary(line.lower().split() for line in open('questions_unified.txt'))
# remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in iteritems(dictionary.dfs) if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # remove stop words and words that appear only once
dictionary.compactify()  # remove gaps in id sequence after words that were removed
dictionary.save('questions_dict.dict')

corpus_gen = (dictionary.doc2bow(line.lower().split()) for line in open('questions_unified.txt'))
corpus = list(corpus_gen)
corpora.MmCorpus.serialize('questions_corpus.mm', corpus)
# following lines are dangerous
# from pprint import pprint
# pprint(corpus)
