from gensim import corpora

dictionary = corpora.Dictionary.load_from_text('D:/Documents/wiki_dump/_wordids.txt.bz2')
print(dictionary)
dictionary.save('wiki_dict.dict')
