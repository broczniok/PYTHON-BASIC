import argparse
import jsonschema
import json
import os
import random
import threading

class JsonSchemaException(Exception):
    pass

class ThreadingException(Exception):
    pass

def get_parser():
    parser = argparse.ArgumentParser(prog="magicgenerator")
    parser.add_argument('--path_to_save_files', required=True, help="Where all files need to be saved", type=argparse.FileType('w'))
    parser.add_argument('--files_count' , help="How much json files to generate")
    parser.add_argument('--file_name', help="What should the files be named (base: file_name)")
    parser.add_argument('--file_prefix', required=True, help="What prefix for file name to use if there is more than 1 file to generate")
    parser.add_argument('--data_schema', required=True, nargs='+', help="It should be string with json schema, could be loaded as path to json file with schema or schema entered to command line")
    parser.add_argument('--data_lines', help="Count of lines for each file (base=1000)")
    parser.add_argument('--clear_path', help="Use if you want to overwrite all other files with same name in chosen directory")
    parser.add_argument('--multiprocessing', help="The number of processes used to create files (base=1)")

def validate_schema(schema: str):
    if os.path.exists(schema):
        with open(schema, "r") as f:
            if jsonschema.validate(f.read()):
                return 1
    elif jsonschema.validate(schema):
        return 2
    else:
        return 0

def handle_schema(schema: str) -> str:
    if validate_schema(schema) == 1:
        result = ""
        with open(schema, "r") as f:
            result = json.load(f)
            return result
    elif validate_schema(schema) == 2:
        return json.load(schema)
    else:
        return ""
    
def generate_json(schema):
    schema_type = schema.get('type')

    schema_type = schema.get('type')

    if schema_type == 'object':
        obj = {}
        properties = schema.get('properties', {})
        for key, value in properties.items():
            obj[key] = generate_json(value)
        return obj

    elif schema_type == 'array':
        item_schema = schema.get('items', {})
        return [generate_json(item_schema)]

    else:
        return None

def write_to_file(filepath: str, files_count: int, file_name: str, file_prefix: str, data_schema: str, data_lines: int, clear_path: str):
    try:
        json_schema = generate_json(data_schema)
    except:
        raise JsonSchemaException("Json schema file error")
        
    complete_path = filepath + file_name + file_prefix + ".json"
    

    for _ in range(0, files_count):
        with open(filepath, "x") as w:
            for _ in range (0, data_lines):
                w.write()


def main(multiprocessing: int):
    if multiprocessing > os.cpu_count():
        multiprocessing = os.cpu_count()
    elif multiprocessing < 0:
        raise ThreadingException("Incorrect amount of threads")
    
    threads = []
    for i in range(multiprocessing):
        thread = threading.Thread(target=write_to_file, name=f'Thread-{i+1}')
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()