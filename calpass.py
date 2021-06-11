import re
import nltk
from nltk.corpus import wordnet
from parser import get_associated_properties, build_query_for
from parser.knowledge_model import synonyms
from parser.question import *
import data.db_access as dba
import data

affirmatives = ["yes", "yeah", "yep", "y", "ye", "correct", "yup"]
exits = ["exit", "quit", "goodbye"]
yesNoQ = ["does", "is"]
regQ = ['what', 'who', 'when']


g = dba.load_db('course_database')

names = dba.query_prof_names(g)
# print(names)

parser = QuestionParser(names=names)

# query = build_query_for(get_associated_properties(parser.entity_extraction_tokenizer('Will Foaad teach CSC-596 next quarter?')))

# print(query)

# rows = g.query(query)

# for r in rows:
#     print(r)

# query = build_query_for(get_associated_properties(parser.entity_extraction_tokenizer('When can I visit ')))

# print(query)

# rows = g.query(query)

# for r in rows:
#     print(r)

# print("Hello, welcome to CalPass. May I have your name, please?")
# user = input("Enter your name: ")
# print("Your name is \'" + user + "\' correct?")
# response = input("Enter your response: ")
# while response.lower().replace(" ", "") not in affirmatives:
#     print("I'm sorry, please tell me your name again.")
#     user = input("Enter your name: ")
#     print("Your name is \'" + user + "\' correct?")
#     response = input("Enter your response: ")
# print("Great! Nice to meet you,", user + "!")
# print("My job is to answer any questions you may have about the CSC and STAT departments here at Cal Poly.")
# print("I specialize in questions about single subjects with single answers, and apologize in advance for any inconveniences caused by these limitations.")
# print("If you have any questions for me, feel free to ask, otherwise enter 'exit' to quit.")
response = input("Enter query: ")

while response.lower().replace(" ", "") not in exits:
    # parse = qp.parse_question(qp, response)
    # print(parse)
    response = input("Enter query: ")
    query = build_query_for(get_associated_properties(parser.entity_extraction_tokenizer(response)))
    print(get_associated_properties(parser.entity_extraction_tokenizer(response)))
    print(query)
    rows = g.query(query)
    print(len(rows))
    for r, _ in zip(rows, range(50)):
        print(r)
print("Thank you for using CalPass,", user + ". Goodbye!")