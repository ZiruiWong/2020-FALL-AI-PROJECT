from gensim import corpora, models, similarities


class tfidf_model:
    def __init__(self, cutSentences=None):
        self.cutSentences = cutSentences  # 分词后的字符串数组
        self.dictionary = None
        self.model = None
        self.index = None

    def modelGene(self):
        """
        生成模型
        :return:
        """
        self.dictionary = corpora.Dictionary(self.cutSentences)
        self.cutSentences = [self.dictionary.doc2bow(sentence) for sentence in self.cutSentences]
        self.model = models.TfidfModel(self.cutSentences)
        self.model.save("model/word2vec.model")

        corpus = self.model[self.cutSentences]
        self.index = similarities.Similarity("modelword2vec.model", corpus, len(self.dictionary))

    def sentence2vec(self, sentence):
        """
        将字符串转变为向量
        :param sentence: 分词后的字符串
        :return: 返回model中的对应值
        """
        vec_bow = self.dictionary.doc2bow(sentence)
        return self.model[vec_bow]

    def similarity_k(self, wordsList, k=5):
        """
        选择最相近的k个答案
        :param wordsList: 分词后的字符串
        :param k: 数值
        :return: 返回索引和相似度
        """
        sentence_vec = self.sentence2vec(wordsList)
        sims = self.index[sentence_vec]

        # 对相似度进行排序 选择前k个答案
        sim_k = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)[:k]

        indexs = [i[0] for i in sim_k]
        scores = [i[1] for i in sim_k]
        return indexs, scores
