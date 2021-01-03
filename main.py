import numpy as np
import pandas as pd
import jieba
import xlrd
import os


class ChatBot:
    def __init__(self, trainSet=None, testSet=None):
        self.trainSet = trainSet
        self.testSet = testSet

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


if __name__ == '__main__':
    cb = ChatBot()
    cb.loadTrainData()
