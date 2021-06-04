import re
from nltk.corpus import wordnet
from parser.question import *

parser = QuestionParser()

parser.entity_extraction_tokenizer('Where is the lab for CSC 456 located?')
parser.entity_extraction_tokenizer('Will Foaad teach csc-456 next quarter?')
parser.entity_extraction_tokenizer('Can I visit Foaad at 12:00?')

parser.entity_extraction_tokenizer('Where are office hours for professor Foaad?')
parser.entity_extraction_tokenizer('Where are Foaad\'s office hours?')
parser.entity_extraction_tokenizer('Who is teaching CSC-456 next quarter?')
parser.entity_extraction_tokenizer('How many 500 level classes does Foaad teach?')
parser.entity_extraction_tokenizer('What time does CSC 456 start on Monday?')

def example_question_cleaning():
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

# print(syn("teach"))