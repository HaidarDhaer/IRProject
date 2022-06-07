def read_documents1():
    f = open("corpus/1/cacm.all")
    merged = ""

    for a_line in f.readlines():
        if a_line.startswith("."):
            merged += "\n" + a_line.strip()
        else:
            merged += " " + a_line.strip()
    # merged = merged.lstrip("\n").split("\n")

    documents = {}

    content = ""
    doc_id = ""

    for a_line in merged.lstrip("\n").split("\n"):
        if a_line.startswith(".I"):
            doc_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".X"):
            documents[doc_id] = content.lstrip(" ")
            with open("corpus/dataset1/" + doc_id + ".text", 'w') as f:
                f.write(documents[doc_id])
            content = ""
            doc_id = ""
        else:
            content += a_line.strip()[3:] + " "
    f.close()
    return documents
