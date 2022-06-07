import re
import math
# read stop words
from Dataset1_processing import get_doc1
import lemmatization
import normalize_doc
import stemming
import vectorMath


def find_relevance_documents(queryVector, diction):
    result = {}
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector = list(value_dic.values())
        result.update({key_dic: vectorMath.get_corner_between_tow_vector(queryVector, vector)})
    return result


def build_vec_mod():
    # read stop words
    f = open("common_words", "r")

    content = f.read()  # content contain stopwords
    # print("content is :",content)
    f.close()
    stop_words = re.findall("\S+", content)

    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    for x in range(1, 3204):
        contentAFile = get_doc1.get_current_doc(x)
        # print("content in A file",x,"is",contentAFile)

        contentAFile = contentAFile.lower()
        contentAFile = normalize_doc.do_normalize(contentAFile)

        # verbs_nouns = filtering_verbs_nouns.filter_verb_nouns(contentAFile)
        # verbs = remove_stop_words.remove_stop_word(verbs_nouns[0], stop_words)
        # nouns = remove_stop_words.remove_stop_word(verbs_nouns[1], stop_words)

        verbs = lemmatization.lemmatiz_for_verb(contentAFile)
        nouns = stemming.nouns_stemming(contentAFile)

        # new step

        termsInAfile.extend(verbs)
        termsInAfile.extend(nouns)

        for w in termsInAfile:
            if w not in tokines:
                tokines.append(w)

        temp_dic = {}  # dictionary for each term
        for y in termsInAfile:  # the key y is the name of term
            temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})
        diction.update({x: temp_dic})

        termsInAfile.clear()
    for a in range(1, 3204):
        temp_dic2 = diction.get(a).copy()
        diction.get(a).clear()

        for y in tokines:
            if y not in temp_dic2.keys():
                diction.get(a).update({y: 0.0})
            else:
                diction.get(a).update({y: temp_dic2[y]})

    f1 = open("vector model1.txt", "w")
    f1.write(str(diction))
    f1.close()

    f2 = open("terms1.txt", "w")
    f2.write(str(tokines))
    f2.close()
    return diction
