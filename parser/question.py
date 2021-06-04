import nltk
import re
import spacy
import numpy as np

from data import variable_pattern, day_pattern

nlp = spacy.load('en_core_web_lg')

class QuestionParser:
    def __init__(self, department_codes=['csc','cpe','stat','ee','laes','data'], names=['Foaad']):
        self.STOP_WORDS = nltk.corpus.stopwords.words()
        self.words_pattern = re.compile(r'([^\s\w]|_)+')
        self.class_pattern = re.compile(r'({depa})(?:-|\s)?(\d{{3}})(?:-|\s)?(\d{{2}})?'.format(depa='|'.join(department_codes)), re.IGNORECASE)
        self.time_pattern = re.compile(r'(\d{1,2})(?=pm|am|:)(?::(\d{2}))?(am|pm)?')
        self.day_pattern = day_pattern
        self.number_pattern = re.compile(r'(\d+)')
        self.names = set([name.lower() for name in names])

    def entity_extraction_tokenizer(self, text):
        tokens = []
        text = self.class_pattern.sub(r' \1-\2-\3 ', text)
        times = self.time_pattern.search(text)
        names = None
        words = nltk.word_tokenize(text)

        for word in words:
            word = word.lower()
            match = self.class_pattern.match(word)
            if match:
                tokens.append(('course', list(match.groups())))
                continue
            match = self.time_pattern.match(word)
            if match:
                tokens.append(('time', list(match.groups())))
                continue
            match = self.day_pattern.match(word)
            if match:
                tokens.append(('day', list(match.groups())))
                continue
            if word in self.names:
                tokens.append(('name', word))
                continue
            match = self.number_pattern.match(word)
            if match:
                tokens.append(('number', list(match.groups())))
                continue

            word = self.words_pattern.sub('', word)
            if len(word) > 0 and word not in self.STOP_WORDS:
                tokens.append((nlp(word)[0].lemma_))
        print(tokens)
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