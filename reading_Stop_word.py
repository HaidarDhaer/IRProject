import re


def read_stop_word():
    f = open("common_words", "r")
    content = f.read()
    # print("1",content)
    f.close()
    stopwords = re.findall("\S+", content)
    # print("stop_words", stopwords)
    return stopwords
