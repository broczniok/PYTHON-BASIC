import json
import os

rootdir = "/Users/broczniok/Desktop/PYTHON-BASIC/practice/5_additional_topics/parsing_serialization_task/source_data"


for folder in os.walk(rootdir):
    for file in folder:
        f = open('2021_09_25.json')
        data = json.load(f)
        print(data)