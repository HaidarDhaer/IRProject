import re
import math
import spacy
from scipy import spatial
import lemmatization
import convert_int_to_string
from Dataset1_processing import get_doc1, get_query1,reading_RLE_Dataset1
from Dataset2_processing import  processing_Query
import normalize_doc
import stemming
import vectorMath

nlp = spacy.load(r'C:\ProgramData\Anaconda3\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.3.0')
nlp2 = spacy.load(r'C:\ProgramData\Anaconda3\Lib\site-packages\en_core_web_lg\en_core_web_lg-3.3.0')

from Dataset2_processing.get_doc import get_current_doc


def find_revelance_documents(queryVector, diction):
    result = {}
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector = list(value_dic.values())
        vector2 = list(value_dic.keys())
        # print("keays",vector2)
        # print("vector=",vector)
        result.update({key_dic: vectorMath.get_corner_between_tow_vector(queryVector, vector)})
    return result


def get_similarity(query_embadding, diction_embadding):
    result = {}
    count = 0.0
    similarity = 0.0
    cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(query_embadding, diction_embadding)
    for key_dic in diction_embadding:
        value_dic = diction_embadding[key_dic]
        vector_key = list(value_dic.keys())
        # print("vector_key",vector_key)
    for word in vector_key:
        new_vector_key_embadding = nlp2.vocab[word].vector
        similarity_for_each_word = cosine_similarity(new_vector_key_embadding, nlp2.vocab[query_embadding].vector)
        count += similarity_for_each_word
    similarity = count / len(vector_key)
    # similarity = count/len(vector_key)
    print(f"similarity {key_dic}", similarity)
    # computed_similarity.append((query_embadding,similarity))
    result.update({key_dic: similarity})
    return result


def get_similarity2(query, diction):
    dic = {}
    text = '\n'.join(query)
    query_embadding = list(nlp(text).vector)
    print(query_embadding)
    # text = ' '.join(query_embadding)
    print("text", text)
    for key_dic in diction:
        value_dic = diction[key_dic]
        vector_key = list(value_dic.keys())
        # print("vector",vector_key)
        # print("query",query)
        # for vector in vector_key:
        text2 = '\n'.join(vector_key)
        diction_embadding = list(nlp(text2).vector)
        # query_embadding = nlp2.vocab[query].vector
        # diction_embadding = nlp2.vocab[vector_key].vector
        result = 1 - spatial.distance.cosine(query_embadding, diction_embadding)
        dic.update({key_dic: result})
    # print("diction",diction_embadding)
    return dic


def convert_to_regular_date(s):
    # s is output ==>   re.findall("regEx",str)
    _date = []
    s1 = ""
    for d in s:
        s1 = d[0]
        s1 += "-"
        if d[1] == "01" or d[1] == "January":
            s1 += "Jan"
        elif d[1] == "02" or d[1] == "February":
            s1 += "Feb"
        elif d[1] == "03" or d[1] == "March":
            s1 += "Mar"
        elif d[1] == "04" or d[1] == "April":
            s1 += "Apr"
        elif d[1] == "05" or d[1] == "May":
            s1 += "May"
        elif d[1] == "06" or d[1] == "June":
            s1 += "Jun"
        elif d[1] == "07" or d[1] == "July":
            s1 += "Jul"
        elif d[1] == "08" or d[1] == "August":
            s1 += "Aug"
        elif d[1] == "09" or d[1] == "September":
            s1 += "Sep"
        elif d[1] == "10" or d[1] == "October":
            s1 += "Oct"
        elif d[1] == "11" or d[1] == "November":
            s1 += "Nov"
        elif d[1] == "12" or d[1] == "December":
            s1 += "Dec"
        else:
            s1 += d[1]

        s1 += "-{}".format(d[2])
        _date.append(s1)
    return _date


def get_vector():
    # after_process_query = processing_Query.query_process()
    tokines = []  # contain all terms for all docs
    termsInAfile = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    reslist = {}
    sortdoc = {}
    doc = {}
    doc_embadding = []
    query_embadding = []
    result_query = []

    for q in range(1, 10):
        current_query = get_query1.get_current_query(q)
        print("current_query", current_query)
        after_process_query = processing_Query.query_process(current_query)
        print("agter peocess query::=", after_process_query)
        for x in range(1, 3204):
            # f = open("corpus/dataset2/{}.text".format(x), "r")
            # contentAFile = f.read()
            # f.close()
            contentAFile = get_doc1.get_current_doc(x)

            ## processing dates
            # extract dates from string
            dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                               "(0[1-9]|1[012])"
                               "[/.-](\d{4})", contentAFile)
            dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                                    "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                                    "[/.-](\d{4})", contentAFile))
            dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                                    "(January|February|March|April|May|June|July|August|September|October|November|December)"
                                    "[/.-](\d{4})", contentAFile))
            years = re.findall("\d{4}", contentAFile)

            # remove dates from string
            contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                                  "(0[1-9]|1[012])"
                                  "[/.-](\d{4})", "", contentAFile)
            contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                                  "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                                  "[/.-](\d{4})", "", contentAFile)
            contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                                  "(January|February|March|April|May|June|July|August|September|October|November|December)"
                                  "[/.-](\d{4})", "", contentAFile)
            contentAFile = re.sub("\d{4}", "", contentAFile)
            # convert dates to regular form 01-Mar-2020
            dates = convert_to_regular_date(dates)

            ## processing emails
            # extract emails from string in contentAFile
            emails = re.findall("\w+@\w+[.]\w+", contentAFile)
            # remove emails from string
            contentAFile = re.sub("\w+@\w+[.]\w+", "", contentAFile)

            ## processing phones
            # extract phones from string in contentAFile
            phones = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                                "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                                "\d{3}[-\.\s]??\d{4})", contentAFile)
            # remove phones from string
            contentAFile = re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                                  "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                                  "\d{3}[-\.\s]??\d{4})", "", contentAFile)
            contentAFile = contentAFile.lower()

            contentAFile = normalize_doc.do_normalize(contentAFile)

            ################################################################################
            verbs = lemmatization.lemmatiz_for_verb(contentAFile)
            nouns = stemming.nouns_stemming(contentAFile)
            termsInAfile.extend(verbs)
            termsInAfile.extend(nouns)
            termsInAfile.extend(years)
            termsInAfile.extend(phones)
            termsInAfile.extend(dates)
            termsInAfile.extend(emails)

            text_doc = ' '.join(termsInAfile)
            text_query = ' '.join(after_process_query)
            doc_embadding = list(nlp2(text_doc).vector)
            query_embadding = list(nlp2(text_query).vector)
            result = 1 - spatial.distance.cosine(doc_embadding, query_embadding)
            if result > 0.5:
                doc.update({x: result})
            # print("result_term with query::", result)
            # array_doc.append((x,result))

            for w in termsInAfile:
                if w not in tokines:
                    tokines.append(w)

            temp_dic = {}  # dictionary for each term
            for y in termsInAfile:
                temp_dic.update({y: (1 + math.log(termsInAfile.count(y), 10)).__round__(5)})
            # print("temp_doc=",temp_dic)

            diction.update({x: temp_dic})
            # print("dictionary",diction)
            print("document number : {} Done".format(x))
            termsInAfile.clear()

        print("document::", doc)
        reslist = sorted(doc.items(), key=lambda item: -item[1])
        # print("reslost", reslist)
        sortdoc = dict(reslist)
        # print("sorted",sortdoc)
        array_for_precision = []
        c = 0
        for r in sortdoc:
            c += 1
            result_query.append(r)
            if c == 5:
                break
            print("num of query", q, "result_query", result_query)
        print("doc", doc)
        print("sort_doc", sortdoc)
        print("doc", doc)
        lenght_of_doc = len(doc)
        lenght_of_result_query = len(result_query)
        print("lenght_of_doc", lenght_of_doc)
        print("sort_doc", sortdoc)
        count_pre_recall = 0
        for i in sortdoc:
            array_for_precision.append(i)
        print("array_for_precision", array_for_precision)
        string = convert_int_to_string.convert(result_query)
        print("string::=", string)
        sortdoc.clear()
        result_query.clear()
        doc.clear()
        mapping = reading_RLE_Dataset1.read_mappings()
        print("mapping value::", mapping['1'])
        count_pr10 = 0
        map_index = mapping[str(q)]
        print("map_index", map_index)
        for i in string:
            if i in map_index:
                count_pr10 = count_pr10 + 1
        print("count", count_pr10)
        array_for_precision_to_string = convert_int_to_string.convert(array_for_precision)
        for i in array_for_precision_to_string:
            if i in map_index:
                count_pre_recall += 1
        print("count_pre_recall", count_pre_recall)
        precision = 0.0
        recall = 0.0
        precision10 = 0.0
        precision = float(count_pre_recall) / float(lenght_of_doc)
        print("precision", precision)
        recall = float(count_pre_recall) / float(len(map_index))
        print("recall", recall)
        precision10 = float(count_pr10) / float(lenght_of_result_query)
        print("precision@10", precision10)
    for a in range(1, 3204):
        temp_dic2 = diction.get(a).copy()
        diction.get(a).clear()
        # print(temp_dic2)
        # for y in list(dict.fromkeys(tokines)):
        for y in tokines:
            if y not in temp_dic2.keys():
                diction.get(a).update({y: 0.0})
            else:
                diction.get(a).update({y: temp_dic2[y]})

            # print("query_doc",query_doc)

    f1 = open("vector model1.txt", "w")
    f1.write(str(diction))
    f1.close()

    f2 = open("terms.txt1", "w")
    f2.write(str(tokines))
    f2.close()
    print(len(tokines))

    # print("sorted_doc",sortdoc)
    # print("query_doc_",query_doc)
    return diction

    # or a, d in reslist:
    #   print(f'num {a} , hsa_similarity {b}')
    # for a, b in query_doc:
    #   print(f'num {a} , with doc {b}')
