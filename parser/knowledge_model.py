import nltk
import spacy
from nltk.corpus import wordnet
from collections import defaultdict

from data.db_access import object_name_map
from util import iterfy

nlp = spacy.load('en_core_web_lg')
STOP_WORDS = nltk.corpus.stopwords.words()

def synonyms(word, min_similarity=0.4):
    input_word = nlp(word)
    list_synonyms = []
    for syn in wordnet.synsets(word):
        syn = [s for s in [syn] + syn.hypernyms() + syn.hyponyms() if s.pos() != 'n']
        for s in syn:
            for lemm in s.lemmas():
                # print(dir(lemm))
                # print(lemm.derivationally_related_forms())
                # print(lemm)
                # print(lemm.name())
                token1 = nlp(lemm.name())
                if token1.vector_norm > 0 and lemm.name() not in STOP_WORDS:
                    sim = input_word.similarity(token1)
                    if sim > min_similarity:
                        list_synonyms.append(lemm.name())
    return sorted(list(set(list_synonyms)))

# one to many name map
object_name_associations = defaultdict(list)
for k, v in object_name_map.items():
    k = iterfy(k)
    words = set()
    for word in k:
        words.add(word)
        for s in synonyms(word):
            words.add(s)
    # print(words)
    for w in words:
        object_name_associations[w].append(v)