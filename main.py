import numpy as np
import pandas as pd
import jieba
import xlrd
import time
import os
import codecs

from Similarity import *



class ChatBot:
    def __init__(self, trainSet=None, testSet=None):
        self.trainSet = trainSet
        self.testSet = testSet
        jieba.load_userdict('./dic/dictionary.txt')
        self.stopwords = set()
        file_obj = codecs.open("./dic/stopword.txt", 'r', 'utf-8')
        while True:
            line = file_obj.readline()
            line = line.strip('\r\n')
            if not line:
                break
            self.stopwords.add(line)
        file_obj.close()
        
    

    def loadTrainData(self):
        # 取data1的问答对
        train1 = pd.read_excel('data/data1.xlsx',engine='openpyxl').iloc[:, :2]
        train1.columns = ["question", "answer"]

        # 取data2的问答对
        train2 = pd.read_excel('data/data2.xlsx',engine='openpyxl').iloc[:, :2]
        train2.columns = ["question", "answer"]

        train = pd.concat([train1, train2], axis=0, ignore_index=True)  # 拼接数据
        self.trainSet = train
        train.drop_duplicates(subset="question", keep='first', inplace=True)  # 数据去重

        # TODO:添加其他的数据处理

        # 保存处理之后的数据为json格式
        train.to_csv('data/qa.csv',header=0,index=0,encoding='utf_8_sig')  #不保存列名,行index，使用utf-8编码
        train.to_json('data/train.txt')

    def loadTestData(self, loadWay=0):
        """
        获取测试数据
        :param loadWay: 数据获取方式，0表示随机选取训练集的一部分，1表示使用已有测试数据
        :return: 返回DataFrame格式的测试集
        """
        # 需要先有一个测试集
        if loadWay == 0:
            # 抽取比例0.2, 取得数据不重复
            self.testSet = self.trainSet.sample(frac=0.2, replace=False).iloc[:, :1]
        else:
            self.testSet = pd.read_json('data/train.txt')
    def read_corpus(self):
        self.qList = []
        self.aList = []
        data = pd.read_csv('./data/qa.csv', header=None).astype(str)
        data_ls = np.array(data).tolist()
        for t in data_ls:
            self.qList.append(t[0])
            self.aList.append(t[1])
    
    # 对句子分词
    def cut(self,sentences,stopword=True):
        seg_list = jieba.cut_for_search(sentences)
        results = []
        for seg in seg_list:
            if stopword and seg in self.stopwords:
                continue
            results.append(seg)
        return results
class Sentence(object):

    def __init__(self,cb,sentence,id=0):
        self.id = id
        self.origin_sentence = sentence
        self.cuted_sentence = ChatBot.cut(cb,self.origin_sentence)

    # 设置该句子得分
    def set_score(self, score):
        self.score = score


if __name__ == '__main__':
    cb = ChatBot()
    cb.loadTrainData()
    cb.read_corpus()#生成问题以及答案的list
    #print('1')
    ss = SentenceSimilarity(cb,cb.qList)
    #print('1')
    ss.TfidfModel()         # tfidf模型
    while True:
        question = input("请输入问题(q退出): ")
        if question == 'q':
            break
        time1 = time.time()
        question_k = ss.similarity_k(question, 5)
        print("亲，我们给您找到的答案是： {}".format(cb.aList[question_k[0][0]]))
        for idx, score in zip(*question_k):
            print("same questions： {},                score： {}".format(cb.qList[idx], score))
        time2 = time.time()
        cost = time2 - time1
        print('Time cost: {} s'.format(cost))

    