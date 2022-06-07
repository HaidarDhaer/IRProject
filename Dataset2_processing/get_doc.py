def get_current_doc(x):
    f = open("corpus/dataset2/{}.text".format(x), "r")
    contentAFile = f.read()
    f.close()
    return contentAFile
