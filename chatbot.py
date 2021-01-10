import pandas as pd
import time
import pickle
from dataProcess import *
from tfidf import *
import json


class ChatBot:
    def __init__(self, qList=None, aList=None):
        self.qList = qList  # 问题列表
        self.aList = aList  # 答案列表

    def loadTrainData(self):
        """
        获取训练数据
        """
        # 取data1的问答对
        train1 = pd.read_excel('data/data1.xlsx', engine='openpyxl').iloc[:, :2]
        train1.columns = ["question", "answer"]

        # 取data2的问答对
        train2 = pd.read_excel('data/data2.xlsx', engine='openpyxl').iloc[:, :2]
        train2.columns = ["question", "answer"]

        # 取data3的问答对
        train3 = pd.read_excel('data/data3.xlsx', engine='openpyxl').iloc[:, :2]
        train3.columns = ["question", "answer"]

        # 将数据进行拼接 并去除问题重复数据
        train = pd.concat([train1, train2, train3], axis=0, ignore_index=True)  # 拼接数据
        train.dropna(inplace=True)  # 去除非数
        train.drop_duplicates(subset="question", keep='first', inplace=True)  # 数据去重
        train.reset_index(inplace=True)  # 重设索引

        # 分开保存问题和答案
        self.qList = train["question"]  # 问题列表
        self.aList = train["answer"]  # 答案列表

    def loadTestData(self, loadWay=1, path='data/test.xlsx'):
        """
        获取测试数据
        :param loadWay: 测试文件生成方式。1：抽取训练集；2：导入训练数据
        :param path: 测试文件路径
        :return:
        """
        if loadWay == 0:
            # 如果不存在测试集，则抽取训练集
            testSet = self.qList.sample(frac=0.2, replace=False)  # 抽取比例0.2, 取得数据不重复
        else:
            # 导入测试集
            testSet = pd.read_excel(path, engine='openpyxl')
            testSet.columns = ["question"]
            rownum = testSet.shape[0]
            testSet[['answer', 'score', '1', '2', '3', '4', '5']] = '' * rownum
        return testSet


def storeData(data, filename):
    """
    保存数据
    :param data: 数据
    :param filename: 文件名
    :return:
    """
    fw = open(filename, 'wb+')
    pickle.dump(data, fw)
    fw.close()


def grabData(filename):
    """
    加载数据
    :param filename: 文件名
    :return:
    """
    fr = open(filename, 'rb')
    return pickle.load(fr)


def preProcess(choice):
    """
    数据预处理
    :return:
    """
    if choice == 'n':
        cb = ChatBot()
        print("[ChatBot]: I'm loading data...")
        cb.loadTrainData()  # 加载训练数据
        storeData(cb, r'model/cb.txt')

        print("           I'm cuting words...")
        s2w = sentence2word()
        cutSentences = cutAllSentences(cb.qList, s2w)  # 进行分词

        print("           I'm training model...")
        tfidf = tfidf_model(cutSentences)
        tfidf.modelGene()  # 生成模型
        storeData(tfidf, r'model/tfidf.txt')
    else:
        print("[ChatBot]: I'm loading data...")
        cb = grabData(r'model/cb.txt')

        print("           I'm cuting words...")
        s2w = sentence2word()

        print("           I'm training model...")
        tfidf = grabData(r'model/tfidf.txt')
    return cb, s2w, tfidf


def questionMode(cb, s2w, tfidf):
    print("[ChatBot]: Entering question mode, you can enter 'q' for quit. >-<")
    while True:
        question = input("           Plz enter question: ")
        if question == 'q':
            break
        time1 = time.time()
        words = cut1Sentence(question, s2w)  # 对问题进行数据处理和分词
        question_k, score = tfidf.similarity_k(words, 5)  # 相似度计算
        print("[ChatBot]: Answer：", cb.aList[question_k[0]])
        for i in range(5):
            print("           related questions：", cb.qList[question_k[i]], "score：", score[i])
        print('           Time cost: ', time.time() - time1)


def fileMode(cb, s2w, tfidf):
    print("[ChatBot]: Entering file mode, you can enter 'q' for quit. >-<")
    path = input("           Plz enter path: ")
    if path != 'q':
        testSet = cb.loadTestData(1)  # 加载测试数据
        cutSentences = cutAllSentences(testSet["question"], s2w)  # 对数据集进行分词处理

        time1 = time.time()
        for i in range(testSet.shape[0]):
            question_k, score = tfidf.similarity_k(cutSentences[i], 5)
            testSet.iloc[i, 1] = cb.aList[question_k[0]]
            testSet.iloc[i, 2] = score[0]
            testSet.iloc[i, 3] = cb.qList[question_k[0]]
            testSet.iloc[i, 4] = cb.qList[question_k[1]]
            testSet.iloc[i, 5] = cb.qList[question_k[2]]
            testSet.iloc[i, 6] = cb.qList[question_k[3]]
            testSet.iloc[i, 7] = cb.qList[question_k[4]]
        print('           Time cost: ', time.time() - time1)
        testSet.to_excel("excel.xlsx")
        jsonSet = testSet[["question", "answer"]].to_json(orient='records',force_ascii=False,lines = True);
        filename='testAnswer.json'
        with open(filename,'w',encoding='utf-8') as file_obj:
            json.dump(jsonSet,file_obj,ensure_ascii=False,sort_keys=False, indent=4)
        #testSet[["question", "answer"]].to_json("testAnswer.json",orient='table')
        print("[ChatBot]: Success store data to 'testAnswer.json'. >-<")


if __name__ == '__main__':
    print("===========TEST BEGIN===========")
    print("[ChatBot]: Hi, I'm Winter Olympic Chatbot >-<")
    print("[ChatBot]: Do you want to use an existed model?")
    choice = input("           Plz enter 'y' or 'n': ")
    cb, s2w, tfidf = preProcess(choice)  # 数据预处理

    print("[ChatBot]: Do you want to ask questions or use a file?")
    choice = input("           Plz enter '1' or '2'(1: Questions 2: A file): ")
    if choice == '1':
        questionMode(cb, s2w, tfidf)
    else:
        fileMode(cb, s2w, tfidf)
