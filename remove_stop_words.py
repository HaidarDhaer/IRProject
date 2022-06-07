def remove_stop_word(t, st):
    clean_data = []
    for l in t:
        if l not in st:
            clean_data.append(l)

    return clean_data
