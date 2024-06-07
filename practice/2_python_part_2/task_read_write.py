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

import os.path

def read_file(path):
    index = 1
    number_table = []
    while True:
        filepath = os.path.join(path, f"file_{index}.txt")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                for x in f:
                    x = x.strip()
                    if x.isdigit():
                        number_table.append(int(x))
            index += 1
        else:
            break
    return number_table

def write_file(number_table, path):
    index = 1
    result = ''
    while True:
        result_filepath = os.path.join(path, f"result_{index}.txt")
        if not os.path.exists(result_filepath):
            with open(result_filepath, "x") as r:
                r.write(str(", ".join(map(str, number_table)) + ", "))
            break
        index += 1

filepath = "/Users/broczniok/Desktop/PYTHON-BASIC/practice/python_part_2/files/"
write_file(read_file(filepath), filepath)
