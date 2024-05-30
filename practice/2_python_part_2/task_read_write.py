"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

from os.path import exists

def read_and_write_to_file():
    index = 1
    number_table = []
    
    while True:
        filepath = "files/file_" + str(index) + ".txt"
        if exists(filepath):
            with open(filepath, "r") as f:
                for x in f:
                    number_table.append(str(x))
        
        index += 1
        if not exists("files/file_" + str(index) + ".txt"):
            break
    
    index = 1
    while True:
        result_filepath = "files/result_" + str(index) + ".txt"
        if not exists(result_filepath):
            with open(result_filepath, "x") as r:
                r.write(", ".join(number_table))
            break
        index += 1

read_and_write_to_file()