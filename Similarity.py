
import numpy as np
from gensim import corpora, models, similarities
from main import Sentence
from collections import defaultdict


class SentenceSimilarity():

    def __init__(self,cb,sentences):
        self.sentences = []
        self.cb = cb
        for i in range(0, len(sentences)):
            self.sentences.append(Sentence(cb,sentences[i], i))

    # 获取切过词的句子
    def get_cuted_sentences(self):
        cuted_sentences = []

        for sentence in self.sentences:
            cuted_sentences.append(sentence.cuted_sentence)

        return cuted_sentences

    # 构建其他复杂模型前需要的简单模型
    def simple_model(self, min_frequency = 1):
        self.texts = self.get_cuted_sentences()

        # 删除低频词
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1
        self.texts = [[token for token in text if frequency[token] > min_frequency] for text in self.texts]
        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus_simple = [self.dictionary.doc2bow(text) for text in self.texts]

    # tfidf模型
    def TfidfModel(self):
        self.simple_model()

        # 转换模型
        self.model = models.TfidfModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]
        self.model.save("./model/word2vec.model")
        # 创建相似度矩阵
        #self.index = similarities.MatrixSimilarity(self.corpus)
        self.index = similarities.Similarity("./model/word2vec.model", self.corpus, len(self.dictionary))



    # 对新输入的句子（比较的句子）进行预处理
    def sentence2vec(self,sentence):
        sentence = Sentence(self.cb,sentence)
        vec_bow = self.dictionary.doc2bow(sentence.cuted_sentence)
        return self.model[vec_bow]


        # 求最相似的句子
    def similarity_k(self, sentence, k):
        sentence_vec = self.sentence2vec(sentence)

        sims = self.index[sentence_vec]
        sim_k = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)[:k]

        indexs = [i[0] for i in sim_k]
        scores = [i[1] for i in sim_k]
        return indexs, scores
