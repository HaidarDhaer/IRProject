import nltk
from nltk import PunktSentenceTokenizer
from nltk.corpus import state_union


def filter_verb_nouns(s):
    train = state_union.raw("2005-GWBush.txt")
    # sample_text = open("corpus/1.txt", "r").read()
    # print(s)
    cust = PunktSentenceTokenizer(train)
    # print("cust",cust)
    tok = cust.tokenize(s)
    # print("tok",tok)

    verbs = []
    nouns = []

    for i in tok:
        words = nltk.word_tokenize(i)
        tag = nltk.pos_tag(words)
        for c in tag:
            if c[1] == "VBD" or c[1] == "VBG" or c[1] == "VBN" or c[1] == "VBN" or c[1] == "VBP" or c[1] == "VBZ" or \
                    c[1] == "VP":
                verbs.append(c[0])
            else:
                nouns.append(c[0])

    return [verbs, nouns]
