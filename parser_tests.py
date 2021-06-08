import re
import nltk
from nltk.corpus import wordnet
from parser import get_associated_properties, build_query_for
from parser.knowledge_model import synonyms
from parser.question import *
import data.db_access as dba
import data


g = dba.load_db('course_database')

names = dba.query_prof_names(g)
print(names)

parser = QuestionParser()

# parser.entity_extraction_tokenizer('Where is the lab for CSC 456 located?')
# parser.entity_extraction_tokenizer('Will Foaad teach csc-456 next quarter?')
# parser.entity_extraction_tokenizer('Can I visit Foaad at 12:00?')

# parser.entity_extraction_tokenizer('Where are office hours for professor Foaad?')
# parser.entity_extraction_tokenizer('Where are Foaad\'s office hours?')
# parser.entity_extraction_tokenizer('Who is teaching CSC-456 next quarter?')
# parser.entity_extraction_tokenizer('How many 500 level classes does Foaad teach?')
# parser.entity_extraction_tokenizer('What time does CSC 456 start on Monday?')

# print(get_associated_properties(parser.entity_extraction_tokenizer('Can I visit Foaad at 12:00?')))
# print(get_associated_properties(parser.entity_extraction_tokenizer('Where are Foaad\'s office hours?')))
# print(get_associated_properties(parser.entity_extraction_tokenizer('Who is teaching CSC-456 next quarter?')))
# print(get_associated_properties(parser.entity_extraction_tokenizer('How many 500 level classes does Foaad teach?')))
# print(get_associated_properties(parser.entity_extraction_tokenizer('What time does CSC 456 start on Monday?')))
# print(get_associated_properties(parser.entity_extraction_tokenizer('Will Foaad teach csc-456 next quarter?')))

parser.parse_question('Will Foaad teach csc-456 next quarter?')

# rows = g.query(build_query_for(get_associated_properties(parser.entity_extraction_tokenizer('Will Foaad teach csc-456 next quarter?'))))

# for r in rows:
#     print(r)

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


# print(synonyms("teach"))