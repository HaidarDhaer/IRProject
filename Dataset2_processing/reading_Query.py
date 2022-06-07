def read_queries2():
    f = open("corpus/2/CISI.QRY")
    merged = ""

    for a_line in f.readlines():
        if a_line.startswith("."):
            merged += "\n" + a_line.strip()
        else:
            merged += " " + a_line.strip()

    queries = {}

    content = ""
    qry_id = ""

    for a_line in merged.split("\n"):
        if a_line.startswith(".I"):
            if not content == "":
                queries[qry_id] = content
            # content = ""
            # qry_id = ""
            qry_id = a_line.split(" ")[1].strip()
        elif a_line.startswith(".W") or a_line.startswith(".T"):
            content += a_line.strip()[3:] + " "
            queries[qry_id] = content.lstrip(" ")
            with open("corpus/Query/" + qry_id + ".text", 'w') as f:
                f.write(queries[qry_id])
            content = ""
            qry_id = ""
            # print(queries[qry_id])
    f.close()
    return queries
