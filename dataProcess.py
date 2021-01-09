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
    sentence = changeChineseNumToArab(sentence)
    seg_list = s2w.seg.cut(sentence)
    results = []
    for word in seg_list:
        if word not in s2w.stopwords:
            results.append(word)
    return results


def cutAllSentences(sentences, s2w):
    return [cut1Sentence(sentence, s2w) for sentence in sentences]

def chinese2digits(uchars_chinese):
    common_used_numerals = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total
 
def changeChineseNumToArab(oriStr):
    num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九',
                        '十']
    more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']
    lenStr = len(oriStr);
    aProStr = ''
    if lenStr == 0:
        return aProStr;
 
    hasNumStart = False;
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True;
 
            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False;
                    aProStr += numResult
 
            aProStr += oriStr[idx]
            pass
 
    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)
 
    return aProStr


if __name__ == '__main__':
    sentences = ["1924年在法国夏蒙尼冬奥会上决出的第一个项目是什么？",
                 "1924年哪位运动员获得了冬奥会历史上第一枚金牌",
                 "1924年夏慕尼冬奥会的地点是什么？",
                 "1924年夏慕尼冬奥会的参赛国家有多少？",
                 "1924年夏慕尼冬奥会的第几届冬奥会？"]

    s2w = sentence2word()
    print(cutAllSentences(sentences, s2w))
