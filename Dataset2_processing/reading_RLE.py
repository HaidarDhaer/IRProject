def read_mappings():
    f = open("corpus/2/CISI.REL")

    mappings = {}

    for a_line in f.readlines():
        voc = a_line.strip().split()
        key = voc[0].strip()
        current_value = voc[1].strip()
        # print("voc = ",voc) # voc is a line
        # print("key = ",key) # key is Query Id
        # print("current_value = ",current_value) #current_value is document id

        value = []
        if key in mappings.keys():
            value = mappings.get(key)
        value.append(current_value)
        mappings[key] = value

    f.close()
    print("mappings is", mappings)
    return mappings
