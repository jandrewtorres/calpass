import numpy as np
import nltk, copy, random
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from .normal_qustion_parser import variable_pattern
import random

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
ps = PorterStemmer()

def getFeatures(inText):
    inText = variable_pattern.sub('', inText)
    tokenized = nltk.word_tokenize(inText)
    tagged = [word[0] for word in nltk.pos_tag(tokenized) if word[1][0] in "N"]
    stemmed  = set([ps.stem(word.lower()) for word in tagged if len(word) > 2])
    print(stemmed)
    return stemmed


def prepare_training_data(masterDB):
    #get positive and negative samples, DATA1 = positive, i.e. words belong to committee id 27
    Data1 = [(getFeatures(example[0]),1) for example in masterDB]
    # Data2 = [(getFeatures(example[0]),0) for example in masterDB if example[1] != "27"]
    random.shuffle(Data1)
    # random.shuffle(Data2)

    #make sure only 500 of each class is chosen for dataset
    allData = Data1
    # allData = Data1[:500]
    # allData.extend(Data2[:500])

    #allData now contains the entire dataset
    random.shuffle(allData)

    #create a big binary vector of all features, baseVector, initialize to 0s
    allFeatures = set()
    for example in allData:
        for f in example[0]:
            allFeatures.add(f)

    print(allFeatures)

    featuresList = list(allFeatures)
    featuresList.sort()
    baseVector = [0 for index in range(len(featuresList))]
    
    data, target = [], []
    #create data and target vectors the way SciKitLearn algorithms expect
    for datum in allData:
        features = copy.deepcopy(baseVector)
        for word in datum[0]:
            features[featuresList.index(word)] = 1
        data.append(features)
        target.append(datum[1])

    #example of what the data looks like
    #print(data[:2],target[:2])
    print("Feature extractions and vectorization done.")
    return data, target

#This function takes in two numpy arrays (data and target) which is the training
#set. It then returns three objects: train_points, train_labels and test. 
#A random portion of data/target pair is removed and put into test in form of
#a list of (features, label) tuples. train_points and train_labels are arrays.
#The remaining portion of data and target are returned unchanged in train.
#It also accepts a split ratio, S, where it means 1/S portion of the data to be 
#put into the test set.
def getDataEn(data, target, S, K):
    if len(data) != len(target):
        return False
    train_points, train_labels, test = [],[],[]
    for label in set(target):
        collection = [row for row in zip(data,target) if row[1] == label]
        random.shuffle(collection)
        splitpoint = len(collection) // S
        test.extend(collection[:splitpoint])
        for row in collection[splitpoint:]:
            train_points.append(row[0])
            train_labels.append(row[1])
    points = []
    labels = []
    for i in range(K):
        train = []
        label = []
        for _ in range(len(train_points)):
            d,t = random.choice(list(zip(train_points, train_labels)))
            train.append(d)
            label.append(t)
        points.append(np.array(train))
        labels.append(np.array(label))
    return points, labels, test


def ensemble_predict(case, classifiers):
    votes = {}
    for classifier in classifiers:
        datum = case[0]
        label = case[1]
        predicted = classifier.predict([datum])[0]
        votes[predicted] = votes.get(predicted, 0) + 1
    max = 0
    predicted = None
    for k, v in votes.items():
        if v > max:
            max = v
            predicted = k
    return predicted


def runTestsEn(test, classifiers):
    true_pos, false_pos, true_neg, false_neg = 0,0,0,0
    correct = 0
    for case in test:
        predicted = ensemble_predict(case, classifiers)
        if predicted == case[1]:
            correct += 1
        # if predicted == 0:
        #     if predicted == label:
        #         true_pos+=1
        #     else:
        #         false_neg+=1
        # else:
        #     if predicted == label:
        #         true_neg+=1
        #     else:
        #         false_pos+=1
    # print("test point: ",datum,"[predicted] truth ==> ",predicted,label)
    print('Accuracy: ' + str(correct / len(test)))
    # precision = true_pos / (true_pos + false_pos)
    precision = correct / len(test)
    recall = 0 #true_pos / (true_pos + false_neg)
    F1 = 0 # (2*precision*recall) / (precision+recall)
    return precision, recall, F1


def train_classifier(masterDB, K=10):
    data, target = prepare_training_data(masterDB)
    train_points, train_labels, test = getDataEn(data, target, 4, K)
    clf = []
    for trains, labels in zip(train_points, train_labels):
        c = tree.DecisionTreeClassifier()
        #clf = GaussianNB()
        c.fit(trains, labels)
        clf.append(c)

    print(f"New Version: K = {K}")
    for train in train_labels:
        for t in list(set(train)):
            print(list(train).count(t),"data points for class",t)
    #print("Accuracy: ",clf.score(np.array([case[0] for case in test]),np.array([case[1] for case in test])))
    precision, recall, F1 = runTestsEn(test, clf)
    print("Precision:",round(precision,2),", Recall:",round(recall,2),", F1:",round(F1,2))
    return clf