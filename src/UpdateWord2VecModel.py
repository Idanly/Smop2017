from gensim import models


def run():
    word2vec_model = models.Word2Vec.load('word2vec_model.w2v')

    def more_sentences():
        return (line.lower().split() for line in open('Ignore\sentences_returned.txt'))

    word2vec_model.build_vocab(more_sentences(), update=True)
    num_sentences_returned = int(open('Ignore\/num_sentences_returned.txt').readline())
    word2vec_model.train(more_sentences(), total_examples=num_sentences_returned)

    word2vec_model.save('word2vec_model.w2v')
    print(word2vec_model)
    print("saved model")
    print(word2vec_model.wv.most_similar(positive=['cat', 'wolf'], negative=['dog']))
    print(word2vec_model.wv.most_similar(positive=['king', 'woman'], negative=['man']))
    print(word2vec_model.wv.doesnt_match("breakfast cereal dinner lunch".split()))
    print(word2vec_model.wv.similarity('woman', 'man'))
