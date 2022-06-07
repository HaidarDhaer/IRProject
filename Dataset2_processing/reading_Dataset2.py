def read_documents2():
    f = open("corpus/2/CISI.ALL")
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
            with open("corpus/dataset2/" + doc_id + ".text", 'w') as f:
                f.write(documents[doc_id])
            content = ""
            doc_id = ""
        else:
            content += a_line.strip()[3:] + " "
    f.close()
    return documents

# with open("corpus/CISI/CISI.ALL") as f:
# lines=""
# for l in f.readlines():
#    lines += "\n" +l.strip() if l.startswith(".") else " " + l.strip()
# lines = lines.lstrip("\n").split("\n")


# n=1
# for l in lines[:n]:
#   print(l)
#
#  print("===================================================")
# doc_set = {}
# doc_id = ""
# doc_auther = ""
# doc_text = ""

# for l in lines:
#   if l.startswith(".I"):
#      doc_id = l.split(" ")[1].strip()
#
#   elif l.startswith(".X"):
#      doc_set[doc_id] = doc_text.lstrip(" ")
#     with open("corpus/"+ doc_id+".text", 'w') as f:
#        f.write(doc_set[doc_id])
#   doc_id = ""
#  doc_text = ""
# else:
#   doc_text += l.strip()[3:]
