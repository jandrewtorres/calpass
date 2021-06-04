import nltk
import re
import spacy
import numpy as np

from data import variable_pattern, day_pattern

STOP_WORDS = nltk.corpus.stopwords.words()
words_pattern = re.compile(r'([^\s\w]|_)+')
class_pattern = re.compile(r'(csc|cpe|stat)(?:-|\s)?(\d{3})')
time_pattern = re.compile(r'^(\d{1,2})(?=pm|am|:)(?::(\d{2}))?(am|pm)?')
# nlp = spacy.load('en_core_web_lg')

def clean_question(question_text):
    sentence = words_pattern.sub('', question_text).lower()
    sentence = class_pattern.sub(r'\1-\2', sentence)
    print(sentence)
    sentence = sentence.split(" ")
    for word in list(sentence):
        if word in STOP_WORDS:
            sentence.remove(word)
    sentence = " ".join(sentence)
    return sentence

def parse_question(question_string):
    original_string = str(question_string)
    question_string = clean_question(question_string)
    print(question_string)
    features = []
    try:
        tokens = nlp(question_string)
        # words = nltk.word_tokenize(original_string)
        # tagged = nltk.pos_tag(words)
        # print(tagged)
        features = [(token.lemma_, nlp(token.lemma_).vector_norm) for token in tokens]
        print(features)

        # print([(pos, word, lemmatizer.lemmatize(word, pos=pos.lower())) for (word, pos) in tagged if pos in ["a", "s", "r", "n", "v"]])
        # namedEnt = nltk.ne_chunk(tagged, binary=True)
        # print(namedEnt)
        # # namedEnt.draw()

    except Exception as e:
        print('error ' + str(e))
    return features