import re


def do_normalize(contentAFile):
    # remove numbers
    contentAFile = re.sub(r'\d+', '', contentAFile)
    # remove all punctuation except words and space
    contentAFile = re.sub(r'[^\w\s]', '', contentAFile)

    # removing last space
    contentAFile = contentAFile[:-1]
    return contentAFile
