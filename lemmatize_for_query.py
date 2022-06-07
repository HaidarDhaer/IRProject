from nltk import WordNetLemmatizer

from remove_stop_words import remove_stop_word
# from processing_Dataset2 import get_stop_word
from reading_Stop_word import read_stop_word
from filtering_verbs_nouns import filter_verb_nouns


def lemmatiz_for_verb(x):
    verbs = get_verbs(x)
    lmtzr = WordNetLemmatizer()
    lemmatizedVerbs = []
    for v in verbs:
        lemmatizedVerbs.append(WordNetLemmatizer().lemmatize(v, 'v'))

    verbs2 = lemmatizedVerbs
    return verbs2


def get_verbs(x):
    stopwords = read_stop_word()
    verbs_nouns = filter_verb_nouns(x)
    verbs = remove_stop_word(verbs_nouns[0], stopwords)
    return verbs
