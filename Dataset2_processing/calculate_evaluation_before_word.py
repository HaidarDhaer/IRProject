import re, math, ast

from Dataset2_processing import get_query, processing_Dataset2, reading_RLE
import lemmatization
import normalize_doc
import stemming
import vectorMath
import convert_int_to_string
from Dataset2_processing import get_dictionary_for_Dataset2


def calculate():
    diction = get_dictionary_for_Dataset2.build_vec_mod()
    f3 = open("terms.txt", "r")
    saved_terms = f3.read()
    f3.close()
    saved_terms = list(ast.literal_eval(saved_terms))

    for Q in range(1, 6):
        q = get_query.get_current_query(Q)
        ## processing the query
        # read stop words
        f = open("common_words", "r")
        content = f.read()
        f.close()
        stop_words = re.findall("\S+", content)

        termsInQuery = []  # this contain all terms in query without stop words
        terms = []  #
        q = q.lower()
        q = normalize_doc.do_normalize(q)

        # verbs_nounes = filtering_verbs_nouns.filter_verb_nouns(q)
        # verbs = remove_stop_words.remove_stop_word(verbs_nounes[0], stop_words)
        # nounes = remove_stop_words.remove_stop_word(verbs_nounes[1], stop_words)

        verbs = lemmatization.lemmatiz_for_verb(q)
        nounes = stemming.nouns_stemming(q)

        termsInQuery.extend(verbs)
        termsInQuery.extend(nounes)
        diction_query = {}  # dictionary for  terms and its frequencies
        for y in termsInQuery:
            diction_query.update({y: (1 + math.log(termsInQuery.count(y), 10)).__round__(5)})

        # remove duplication from termsInQuery
        tempTerms = []
        for w in termsInQuery:
            if w not in tempTerms:
                tempTerms.append(w)

        termsInQuery = tempTerms

        # # Extension of the previous diction in order to contain all terms
        # # and show their repetition within the query
        temp_dic2 = diction_query.copy()
        diction_query.clear()

        for term in saved_terms:
            if term not in temp_dic2.keys():
                diction_query.update({term: 0.0})
            else:
                diction_query.update({term: temp_dic2[term]})
                # diction_query.update({y: 505})

        # for x, y in diction_query.items():
        #     print(x," ====> ", y)

        # # check if vector of the query is zero or not , if was zero that mean the query
        # # will not return any results
        len_vec_query = vectorMath.calculate_length_vector(list(diction_query.values()))
        if len_vec_query != 0.0:
            doc = processing_Dataset2.find_revelance_documents(list(diction_query.values()), diction)
            result_query = []
            print("result::", doc)

            reslist = sorted(doc.items(), key=lambda item: item[1])
            # print("reslost", reslist)
            sortdoc = dict(reslist)
            # print("sorted",sortdoc)
            array_for_precision = []
            c = 0
            for r in sortdoc:
                c += 1
                result_query.append(r)
                if c == 11:
                    break
                print("num of query", Q, "result_query", result_query)
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
            ###############3
            mapping = reading_RLE.read_mappings()
            count_pr10 = 0
            map_index = mapping[str(Q)]
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
