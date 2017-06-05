from nltk.corpus import wordnet as wn
data = [('When was Hitchcock born?', wn.synset('year.n.01')),
        ('Where was Hitchcock born?', wn.synset('city.n.01')),
        ('How many Oscar awards did Hitchcock win?', wn.synset('number.n.01')),
        ('When did Hitchcock die?', wn.synset('year.n.01')),
        ('Where did Hitchcock die?', wn.synset('city.n.01')),
        ('What year was Christopher Reeve paralyzed?', wn.synset('year.n.01')),
        ('How many "Superman" movies did he make?' ,wn.synset('number.n.01')),
        ('During what years were these "Superman" movies made?',wn.synset('year.n.01')),
        ('Which actress co-starred in the most "Superman" movies with Reeve?', wn.synset('person.n.01')),
        ('What year did Reeve commence his theatrical career?' ,wn.synset('year.n.01')),
        ('Hugo Chavez is president of which country?', wn.synset('country.n.01')),
        ('How old was Hugo Chavez when first elected?', wn.synset('number.n.01')),
        ('Where did Chavez graduate from?', wn.synset('place.n.01')),
        ('What percentage of the 2000 Presidential vote did Chavez receive?', wn.synset('number.n.01')),
        ('Who was Chavezs opponent in his 1998 Presidential race?', wn.synset('person.n.01')),
        ('Who founded NASCAR?', wn.synset('person.n.01')),
        ('When was NASCAR founded?' ,wn.synset('year.n.01')),
        ('Who took control of NASCAR from the founder?', wn.synset('person.n.01')),
        ('How much money does NASCAR generate from TV rights annually?', wn.synset('number.n.01')),
        ('What was the number of member nations of the U.N. in 2000?', wn.synset('number.n.01')),
        ('How many non-permanent members are in the Security Council?', wn.synset('number.n.01')),
        ('Who was the President of the U.N. Security Council for August 1999?', wn.synset('person.n.01')),
        ('Who became Tufts University President in 1992?', wn.synset('person.n.01')),
        ('What year was Wal-Mart founded?', wn.synset('year.n.01')),
        ('Who founded Wal-Mart?', wn.synset('person.n.01')),
        ('How many Wal-Mart employees are there in the U.S.?', wn.synset('number.n.01')),
        ('How many stores does Wal-Mart operate world-wide?',  wn.synset('number.n.01')),
        ('How many Wal-Mart outlets are there in India?', wn.synset('number.n.01')),
        ('Which country received the largest loan ever granted by the IMF?', wn.synset('country.n.01')),
        ('When was the IMF founded?', wn.synset('year.n.01')),
        ('Where is the IMF headquartered?', wn.synset('city.n.01'))]