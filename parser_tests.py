import re
from nltk.corpus import wordnet
from parser.question import *

# parse_question('Where is the lab for CSC 456 located?')
# parse_question('Will Foaad teach csc-456 next quarter?')
# parse_question('Where are office hours for professor Foaad?')
# parse_question('Where are Foaad\'s office hours?')
# parse_question('Who is teaching CSC-456 next quarter?')
# parse_question('How many 500 level classes does Foaad teach?')
# parse_question('Can I visit Foaad at 12:00?')

def question_cleaning():
    questions = []
    with open('data/extracted_data/questions.txt', mode='r') as qfile:
        for line in qfile:
            questions.append(line)

    words = []
    for q in questions:
        q = variable_pattern.sub('', q).lower()
        q = words_pattern.sub('', q)
        for t in nltk.word_tokenize(q):
            if t not in STOP_WORDS:
                words.append(t.lower())

    words = nltk.FreqDist(words)
    word_features = list(words.keys())[:3000]

    print(word_features)

def syn(word):
    list_synonyms = []
    for syn in wordnet.synsets(word):
        for lemm in syn.lemmas(): 
            print(dir(lemm))
            print(lemm.derivationally_related_forms())
            print(lemm)
            list_synonyms.append(lemm.name())
    return sorted(list(set(list_synonyms)))

print(syn("teach"))