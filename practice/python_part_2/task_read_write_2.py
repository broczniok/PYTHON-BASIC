"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""
from os.path import exists

def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words

def write_to_file_utf(path):
    index = 1
    table = generate_words()
    while(True):
        if not exists(str(path)+ "/file_" + str(index) + ".txt"):
            filepath = str(path)+ "/file_" + str(index) + ".txt"
            f = open(filepath, "x", encoding="UTF-8")
            for item in table:
                f.write(item+'\n')
            f.close()
            break
        
        index += 1

def write_to_file_cp1252(path):
    index = 1
    table = generate_words()
    while(True):
        if not exists(str(path)+ "/file_" + str(index) + ".txt"):
            filepath = str(path)+ "/file_" + str(index) + ".txt"
            f = open(filepath, "x", encoding="CP1252")
            for item in list(reversed(table)):
                f.write(item + ',')
            f.close()
            break
        index += 1

    


write_to_file_utf("files")
write_to_file_cp1252("files")