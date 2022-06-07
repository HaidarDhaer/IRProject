import lemmatize_for_query
import normalize_doc
import stem_for_query
import re


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


def query_process(contentAQuery):
    tokines = []  # contain all terms for all docs
    termsInAQuery = []  # this contains all terms in (current file) without stop words
    diction = {}  # dictionary for all tokens
    # for q in range(1, 100):
    # f = open("corpus/dataset2/{}.text".format(x), "r")
    # contentAFile = f.read()
    # f.close()
    # contentAQuery=get_current_query.get_current_query(q)

    ## processing dates
    # extract dates from string
    dates = re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                       "(0[1-9]|1[012])"
                       "[/.-](\d{4})", contentAQuery)
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                            "[/.-](\d{4})", contentAQuery))
    dates.extend(re.findall("(0[1-9]|[12]\d|3[01])[/.-]"
                            "(January|February|March|April|May|June|July|August|September|October|November|December)"
                            "[/.-](\d{4})", contentAQuery))
    years = re.findall("\d{4}", contentAQuery)

    # remove dates from string
    contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(0[1-9]|1[012])"
                          "[/.-](\d{4})", "", contentAQuery)
    contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
                          "[/.-](\d{4})", "", contentAQuery)
    contentAFile = re.sub("(0[1-9]|[12]\d|3[01])[/.-]"
                          "(January|February|March|April|May|June|July|August|September|October|November|December)"
                          "[/.-](\d{4})", "", contentAQuery)
    contentAFile = re.sub("\d{4}", "", contentAQuery)
    # convert dates to regular form 01-Mar-2020
    dates = convert_to_regular_date(dates)

    ## processing emails
    # extract emails from string in contentAFile
    emails = re.findall("\w+@\w+[.]\w+", contentAQuery)
    # remove emails from string
    contentAFile = re.sub("\w+@\w+[.]\w+", "", contentAQuery)

    ## processing phones
    # extract phones from string in contentAFile
    phones = re.findall("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                        "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                        "\d{3}[-\.\s]??\d{4})", contentAQuery)
    # remove phones from string
    contentAFile = re.sub("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4} | "
                          "\(\d{3}\)\s *\d{3}[-\.\s]??\d{4} |"
                          "\d{3}[-\.\s]??\d{4})", "", contentAQuery)
    contentAFile = contentAFile.lower()

    contentAFile = normalize_doc.do_normalize(contentAFile)

    # verbs_nouns =filter_verb_nouns(contentAFile)
    # print("befor remove stop word",verbs_nouns[1])
    # verbs = remove_stop_word(verbs_nouns[0],stopwords)
    # nouns = remove_stop_word(verbs_nouns[1],stopwords)
    # print("verbs=", verbs)
    # print("/////////////////////////////////////////")
    # print("nouns=", nouns)
    ################################################################################
    verbs = lemmatize_for_query.lemmatiz_for_verb(contentAQuery)
    nouns = stem_for_query.nouns_stemming(contentAQuery)

    termsInAQuery.extend(verbs)
    termsInAQuery.extend(nouns)
    termsInAQuery.extend(years)
    termsInAQuery.extend(phones)
    termsInAQuery.extend(dates)
    termsInAQuery.extend(emails)
    tempTerms = []
    for w in termsInAQuery:
        if w not in tempTerms:
            tempTerms.append(w)
        # print("term in a filr",termsInAfile)
        # embad_for_term=nlp(str(termsInAfile)).vector
        # print("word embadding for term in a file",embad_for_term)
        # text1 = "What problems and concerns are there in making up descriptive titles? What difficulties are involved in automatically retrieving articles from approximate titles? What is the usual relevance of the content of articles to their titles?"
        # text1 = "How can actually pertinent data, as opposed to references or entire articles themselves, be retrieved automatically in response to information requests?"
        # text = ' '.join(termsInAfile)
        # text1_embadding = list(nlp2(text1).vector)
        # term_embadding = list(nlp2(text).vector)
        # result = 1 - spatial.distance.cosine(text1_embadding, term_embadding)
        # print("result_term with query::", result)

    return tempTerms
