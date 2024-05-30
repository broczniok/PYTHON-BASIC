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

def write_to_file():
    index = 1
    table = generate_words()
    
    while True:
        file_path = f"files/file_{index}.txt"
        if not exists(file_path):
            with open(file_path, "x", encoding="utf-8") as f:
                result = '\n'.join(table) + '\n'
                f.write(result)
            
            reverse_file_path = f"files/reversed_file_{index}.txt"
            with open(reverse_file_path, "x", encoding="cp1252") as f_reversed:
                reversed_result = ','.join(reversed(table))+','
                f_reversed.write(reversed_result)
            return
        
        index += 1

write_to_file()