import data.extracted_data.classifier as classifier
import data.extracted_data.normal_qustion_parser as nqp

masterDB = nqp.load_question_file('data/extracted_data/questions.json')
masterDB = [(x, y[1]) for x, y in masterDB]
print(masterDB[:10])
classifier.train_classifier(masterDB)

