import re
from itertools import islice

trec_8 = open('trec-8.txt', 'r')
trec_9 = open('trec-9.txt', 'r')
trec_questions = open('trec_questions.txt', 'w')

punct_pattern = re.compile('[,\.!?:"]')
underscore_patten = re.compile('[_]{2,}')
space_pattern = re.compile('[ ]{2,}')

# Getting trec-8 questions
while True:
    next_n_lines = list(islice(trec_8, 10))
    if not next_n_lines:
        break
    question = space_pattern.sub(' ', underscore_patten.sub('what', punct_pattern.sub('', next_n_lines[5])))
    trec_questions.write(question)
# Getting trec-9 questions
while True:
    next_n_lines = list(islice(trec_9, 10))
    if not next_n_lines:
        break
    question = space_pattern.sub(' ', underscore_patten.sub('what', punct_pattern.sub('', next_n_lines[5])))
    trec_questions.write(question)

    # Finished
