from nltk.stem import PorterStemmer

from reading_Stop_word import read_stop_word
from filtering_verbs_nouns import filter_verb_nouns
from remove_stop_words import remove_stop_word


def nouns_stemming(x):
    nouns = get_nouns(x)
    stem = PorterStemmer()
    PorterNouns = []
    for n in nouns:
        PorterNouns.append(stem.stem(n))
    nouns2 = PorterNouns
    return nouns2


def get_nouns(x):
    stopwords = read_stop_word()
    verbs_nouns = filter_verb_nouns(x)
    nouns = remove_stop_word(verbs_nouns[1], stopwords)
    return nouns
