def get_current_query(q):
    with open("corpus/Query/{}.text".format(q), "r") as f:
        contentAQuery = f.read()
        f.close()
    return contentAQuery
