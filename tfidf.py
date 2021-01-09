from collections import defaultdict
from gensim import corpora, models, similarities


class tfidf_model:
    def __init__(self, cutSentences=None):
        self.cutSentences = cutSentences
        self.dictionary = None
        self.model = None
        self.index = None

    def modelGene(self, min_frequency=1):

        '''frequency = defaultdict(int)
        for sentence in self.cutSentences:
            for word in sentence:
                frequency[word] += 1
        self.cutSentences = [[word for word in sentence if frequency[word] > min_frequency] for sentence in
                             self.cutSentences]
        '''
        self.dictionary = corpora.Dictionary(self.cutSentences)
        self.cutSentences = [self.dictionary.doc2bow(sentence) for sentence in self.cutSentences]
        self.model = models.TfidfModel(self.cutSentences)
        self.model.save("model/word2vec.model")

        corpus = self.model[self.cutSentences]
        self.index = similarities.Similarity("modelword2vec.model", corpus, len(self.dictionary))

    def sentence2vec(self, sentence):
        vec_bow = self.dictionary.doc2bow(sentence)
        return self.model[vec_bow]

        # 求最相似的句子

    def similarity_k(self, wordsList, k=5):
        sentence_vec = self.sentence2vec(wordsList)

        sims = self.index[sentence_vec]
        sim_k = sorted(enumerate(sims), key=lambda item: item[1], reverse=True)[:k]

        indexs = [i[0] for i in sim_k]
        scores = [i[1] for i in sim_k]
        return indexs, scores
