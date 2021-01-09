import pandas as pd
import time
import pickle
from dataProcess import *
from tfidf import *


class ChatBot:
    def __init__(self, qList=None, aList=None, testSet=None):
        self.qList = qList
        self.aList = aList
        self.testSet = testSet

    def loadTrainData(self):
        # 取data1的问答对
        train1 = pd.read_excel('data/data1.xlsx', engine='openpyxl').iloc[:, :2]
        train1.columns = ["question", "answer"]

        # 取data2的问答对
        train2 = pd.read_excel('data/data2.xlsx', engine='openpyxl').iloc[:, :2]
        train2.columns = ["question", "answer"]

        # 数据处理
        # 将数据进行拼接 并去除问题重复数据
        train = pd.concat([train1, train2], axis=0, ignore_index=True)  # 拼接数据
        train.dropna(inplace=True)
        train.drop_duplicates(subset="question", keep='first', inplace=True)  # 数据去重
        train.reset_index(inplace=True)

        # 分开保存问题和答案
        self.qList = train["question"]
        self.aList = train["answer"]

    def loadTestData(self, loadWay=1):
        """
        获取测试数据
        :param loadWay: 数据获取方式，0表示随机选取训练集的一部分，1表示使用已有测试数据
        :return: 返回DataFrame格式的测试集
        """
        # 需要先有一个测试集
        if loadWay == 0:
            # 抽取比例0.2, 取得数据不重复
            self.testSet = self.qList.sample(frac=0.2, replace=False)
        else:
            testSet = pd.read_excel('data/test.xlsx', engine='openpyxl')
            testSet.columns = ["question"]
            rownum = testSet.shape[0]
            testSet[['answer', 'score', '1', '2', '3', '4', '5']] = '' * rownum
            self.testSet = testSet


def storeData(data, filename):
    fw = open(filename, 'wb+')
    pickle.dump(data, fw)
    fw.close()


def grabData(filename):
    fr = open(filename, 'rb')
    return pickle.load(fr)


def preProcess():
    choice = input("           Plz enter 'y' or 'n': ")
    if choice == 'n':
        cb = ChatBot()
        print("[ChatBot]: I'm loading data...")
        cb.loadTrainData()
        storeData(cb, r'model/cb.txt')

        print("           I'm cuting words...")
        s2w = sentence2word()
        cutSentences = cutAllSentences(cb.qList, s2w)

        print("           I'm training model...")
        tfidf = tfidf_model(cutSentences)
        tfidf.modelGene()
        storeData(tfidf, r'model/tfidf.txt')
    else:
        cb = grabData(r'model/cb.txt')
        s2w = sentence2word()
        tfidf = grabData(r'model/tfidf.txt')
    return cb, s2w, tfidf


def questionMode(cb, s2w, tfidf):
    print("[ChatBot]: Entering question mode, you can enter 'q' for quit. >-<")
    while True:
        question = input("[ChatBot]: Plz enter question: ")
        if question == 'q':
            break
        time1 = time.time()
        words = cut1Sentence(question, s2w)
        question_k, score = tfidf.similarity_k(words, 5)
        print("[ChatBot]: Answer：",cb.aList[question_k[0]])
        for i in range(5):
            print("           related questions",cb.qList[question_k[i]],"score：",score[i])
        time2 = time.time()
        cost = time2 - time1
        print('           Time cost: {} s'.format(cost))


def fileMode(cb, s2w, tfidf):
    print("[ChatBot]: Entering file mode, you can enter 'q' for quit. >-<")
    question = input("           Plz enter path: ")
    if question != 'q':
        cb.loadTestData()
        cutSentences = cutAllSentences(cb.testSet["question"], s2w)

        time1 = time.time()
        for i in range(cb.testSet.shape[0]):
            #print("          ", i, "/", cb.testSet.shape[0] - 1)
            question_k, score = tfidf.similarity_k(cutSentences[i], 5)
            cb.testSet.iloc[i, 1] = cb.aList[question_k[0]]
            cb.testSet.iloc[i, 2] = score[0]
            cb.testSet.iloc[i, 3] = cb.qList[question_k[0]]
            cb.testSet.iloc[i, 4] = cb.qList[question_k[1]]
            cb.testSet.iloc[i, 5] = cb.qList[question_k[2]]
            cb.testSet.iloc[i, 6] = cb.qList[question_k[3]]
            cb.testSet.iloc[i, 7] = cb.qList[question_k[4]]
        time2 = time.time()
        cost = time2 - time1
        print('           Time cost: {} s'.format(cost))
        cb.testSet.to_excel("excel.xlsx")


if __name__ == '__main__':
    print("===========TEST BEGIN===========")
    print("[ChatBot]: Hi, I'm Winter Olympic Chatbot >-<")
    print("[ChatBot]: Do you want to use an existing model?")
    cb, s2w, tfidf = preProcess()

    print("[ChatBot]: Do you want to ask questions or use a file?")
    choice = input("           Plz enter '1' or '2'(1: Questions 2: A file): ")
    if choice == '1':
        questionMode(cb, s2w, tfidf)

    else:
        fileMode(cb, s2w, tfidf)
    

