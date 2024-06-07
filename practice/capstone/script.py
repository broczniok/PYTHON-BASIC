import argparse
import jsonschema
import json
import os
import random
import threading
from configparser import ConfigParser

class JsonSchemaException(Exception):
    pass

class ThreadingException(Exception):
    pass

def get_parser():

    config = ConfigParser()
    try:
        config.read("default.ini")
    except:
        print("default.ini reading went wrong")
        raise SystemExit()

    parser = argparse.ArgumentParser(prog="magicgenerator")
    parser.add_argument('--path_to_save_files', metavar="pathfile",required=True, help="Where all files need to be saved", type=str)
    parser.add_argument('--files_count', metavar="file_count",  help="How much json files to generate", type=int)
    parser.add_argument('--file_name', metavar="file_name", help="What should the files be named (base: file_name)", type=str)
    parser.add_argument('--file_prefix', metavar="file_prefix", help="What prefix for file name to use if there is more than 1 file to generate", type=str)
    parser.add_argument('--data_schema', metavar="data_schema", required=True, nargs='+', help="It should be string with json schema, could be loaded as path to json file with schema or schema entered to command line", type=str)
    parser.add_argument('--data_lines', metavar="data_lines", help="Count of lines for each file (base=1000)", type=int)
    parser.add_argument('--clear_path', metavar="clear_path", help="Use if you want to overwrite all other files with same name in chosen directory")
    parser.add_argument('--multiprocessing', metavar="multiprocessing", help="The number of processes used to create files (base=1)", type=int)

    args = parser.parse_args()
    

    pathfile = args.path_to_save_files
    files_count = args.files_count
    file_name = args.file_name
    file_prefix = args.file_prefix
    data_schema = args.data_schema
    data_lines = args.data_lines
    clear_path = args.clear_path
    multiprocessing = args.multiprocessing

    if args.files_count is not None:
        files_count = args.files_count
    else:
        files_count = int(config["DEFAULT"]["files_count"])
    
    if args.file_name is not None:
        file_name = args.file_name
    else:
        file_name = str(config["DEFAULT"]["file_name"])

    if args.data_lines is not None:
        data_lines = args.data_lines
    else:
        data_lines = int(config["DEFAULT"]["data_lines"])

    if args.clear_path is not None:
        clear_path = args.clear_path
    else:
        clear_path = str(config["DEFAULT"]["clear_path"])
    
    if args.file_prefix is not None:
        file_prefix = args.file_prefix
    else: 
        file_prefix = str(config["DEFAULT"]["file_prefix"])

    if args.multiprocessing is not None:
        multiprocessing = args.multiprocessing
    else:
        multiprocessing = int(config["DEFAULT"]["multiprocessing"])

    print("pathfile:",pathfile)
    print("files conut:",files_count)
    print("file name:",file_name)
    print("data schema:", data_schema)
    print("data lines:",data_lines)
    print("clear path:",clear_path)
    print("file prefix", file_prefix)
    print("multiprocessing", multiprocessing)


    
    print("Working")







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

get_parser()