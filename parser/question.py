import nltk
import re
import spacy
import numpy as np

from data import variable_pattern, day_pattern, time_pattern, words_pattern
import data.db_access as dba 
from .knowledge_model import nlp, STOP_WORDS

class QuestionParser:
    def __init__(self, department_codes=['csc','cpe','stat','ee','laes','data'], names=['Foaad']):
        self.words_pattern = words_pattern
        self.class_pattern = re.compile(r'({depa})(?:-|\s)?(\d{{3}})(?:-|\s)?(\d{{2}})?'.format(depa='|'.join(department_codes)), re.IGNORECASE)
        self.time_pattern = time_pattern
        self.day_pattern = day_pattern
        self.number_pattern = re.compile(r'(\d+)')
        self.names = set([name.lower() for name in names])

    def detect_name(self, word):
        if len(word) > 2:
            for n in self.names:
                try:
                    nin = re.search(r'({word})'.format(word=word), n, re.IGNORECASE)
                    if nin:
                        return n
                except Exception as e:
                    continue
        return False

    def entity_extraction_tokenizer(self, text):
        tokens = []
        text = self.class_pattern.sub(r' \1-\2-\3 ', text)
        words = nltk.word_tokenize(text)

        for word in words:
            word = word.lower()
            match = self.class_pattern.match(word)
            if match:
                tokens.append((dba.calpass_course_properties.course_name, list(match.groups())))
                continue
            match = self.time_pattern.match(word)
            if match:
                tokens.append(('time', list(match.groups())))
                continue
            match = self.day_pattern.match(word)
            if match:
                tokens.append(('day', list(match.groups())))
                continue
            name = self.detect_name(word)
            if name:
                tokens.append((dba.calpass_professor_properties.personName, name))
                continue
            match = self.number_pattern.match(word)
            if match:
                tokens.append(('number', list(match.groups())))
                continue

            word = self.words_pattern.sub('', word)
            if len(word) > 0 and word not in STOP_WORDS:
                tokens.append((nlp(word)[0].lemma_))
        # print(tokens)
        return tokens

    def clean_question(self, question_text):
        sentence = words_pattern.sub('', question_text).lower()
        print(sentence)
        sentence = sentence.split(" ")
        for word in list(sentence):
            if word in STOP_WORDS:
                sentence.remove(word)
        sentence = " ".join(sentence)
        return sentence

    def parse_question(self, question_string):
        original_string = str(question_string)
        question_string = self.clean_question(question_string)
        print(question_string)
        features = []
        try:
            tokens = nlp(question_string)
            # words = nltk.word_tokenize(original_string)
            # tagged = nltk.pos_tag(words)
            # print(tagged)
            features = [(token.lemma_, nlp(token.lemma_).vector_norm, token.pos_) for token in tokens]
            print(features)

            # print([(pos, word, lemmatizer.lemmatize(word, pos=pos.lower())) for (word, pos) in tagged if pos in ["a", "s", "r", "n", "v"]])
            # namedEnt = nltk.ne_chunk(tagged, binary=True)
            # print(namedEnt)
            # # namedEnt.draw()

        except Exception as e:
            print('error ' + str(e))
        return features