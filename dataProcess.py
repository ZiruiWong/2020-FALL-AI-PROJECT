import sys
import unicodedata as ud
import pkuseg


class sentence2word:
    def __init__(self):
        self.stopwords = [line.strip() for line in open('./dic/stopword.txt', 'rb').readlines()]
        self.punctuation = dict.fromkeys(i for i in range(sys.maxunicode) if ud.category(chr(i)).startswith('P'))  # 符号集
        self.seg = pkuseg.pkuseg()


def cut1Sentence(sentence, s2w):
    # print(sentence)
    sentence = sentence.strip()  # 去除字符串两端空格
    sentence = sentence.translate(s2w.punctuation)  # 去除标点符号
    seg_list = s2w.seg.cut(sentence)
    results = []
    for word in seg_list:
        if word not in s2w.stopwords:
            results.append(word)
    return results


def cutAllSentences(sentences, s2w):
    return [cut1Sentence(sentence, s2w) for sentence in sentences]


if __name__ == '__main__':
    sentences = ["1924年在法国夏蒙尼冬奥会上决出的第一个项目是什么？",
                 "1924年哪位运动员获得了冬奥会历史上第一枚金牌",
                 "1924年夏慕尼冬奥会的地点是什么？",
                 "1924年夏慕尼冬奥会的参赛国家有多少？",
                 "1924年夏慕尼冬奥会的第几届冬奥会？"]

    s2w = sentence2word()
    print(cutAllSentences(sentences, s2w))
