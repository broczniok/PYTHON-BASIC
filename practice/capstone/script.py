import argparse
import jsonschema
from faker import Faker
import uuid
import time
import logging
import json
import os
import random
import threading
from configparser import ConfigParser

class JsonSchemaException(Exception):
    pass

class ThreadingException(Exception):
    pass

def fill_parser(config, args):
    result = {"pathfile":[], "files_count": [], "file_name": [],"data_schema": [], "data_lines": [], "clear_path": [], "file_prefix": [], "multiprocessing": []}

    result["pathfile"].append(args.path_to_save_files)
    result["data_schema"].append(args.data_schema)

    if args.files_count is not None:
        result["files_count"].append(args.files_count)
    else:
        result["files_count"].append(int(config["DEFAULT"]["files_count"]))

    if args.file_name is not None:
        result["file_name"].append(args.file_name)
    else:
        result["file_name"].append(str(config["DEFAULT"]["file_name"]))


    if args.data_lines is not None:
        result["data_lines"].append(args.data_lines)
    else:
        result["data_lines"].append(int(config["DEFAULT"]["data_lines"]))


    if args.clear_path is not None:
        result["clear_path"].append(args.clear_path)

    else:
        result["clear_path"].append(str(config["DEFAULT"]["clear_path"]))


    if args.file_prefix is not None:
        result["file_prefix"].append(args.file_prefix)

    else:
        result["file_prefix"].append(str(config["DEFAULT"]["file_prefix"]))


    if args.multiprocessing is not None:
        result["multiprocessing"].append(args.multiprocessing)
    else:
        result["multiprocessing"].append(int(config["DEFAULT"]["multiprocessing"]))



    return result


def get_parser():

    config = ConfigParser()
    try:
        config.read("default.ini")
    except:
        print("default.ini file reading went wrong")
        raise SystemExit()

    parser = argparse.ArgumentParser(prog="magicgenerator", description="Capstone Project function that generates fake JSON files from command line.")
    parser.add_argument('--path_to_save_files', metavar="pathfile",required=True, help="Where all files need to be saved", type=str)
    parser.add_argument('--files_count', metavar="file_count",  help="How much json files to generate", type=int)
    parser.add_argument('--file_name', metavar="file_name", help="What should the files be named (base: file_name)", type=str)
    parser.add_argument('--file_prefix', metavar="file_prefix", help="What prefix for file name to use if there is more than 1 file to generate", type=str)
    parser.add_argument('--data_schema', metavar="data_schema", required=True, nargs='+', help="It should be string with json schema, could be loaded as path to json file with schema or schema entered to command line", type=str)
    parser.add_argument('--data_lines', metavar="data_lines", help="Count of lines for each file (base=1000)", type=int)
    parser.add_argument('--clear_path', metavar="clear_path", help="Use if you want to overwrite all other files with same name in chosen directory")
    parser.add_argument('--multiprocessing', metavar="multiprocessing", help="The number of processes used to create files (base=1)", type=int)

    args = parser.parse_args()

    arguments = fill_parser(config, args)

    print("pathfile:",arguments["pathfile"][0])
    print("files count:",arguments["files_count"][0])
    print("file name:",arguments["file_name"][0])
    print("data schema:", arguments["data_schema"][0])
    print("data lines:",arguments["data_lines"][0])
    print("clear path:",arguments["clear_path"][0])
    print("file prefix", arguments["file_prefix"][0])
    print("multiprocessing", arguments["multiprocessing"][0])

    if validate_schema(str(arguments["data_schema"][0])) != 0:
        print(parse_schema(handle_schema(str(arguments["data_schema"][0]))))
    else:
        print("Invalid schema")



    print("Working")



def parse_schema(schema_str):
    schema = json.loads(schema_str)
    data = {}

    for key, value in schema.items():
        try:
            type_hint, generation_rule = value.split(":", 1)
        except ValueError:
            raise ValueError(f"Invalid schema format for key '{key}': missing ':' separator")

        if type_hint == "timestamp":
            if generation_rule:
                logging.warning(f"Timestamp type does not support any values. Value for '{key}' will be ignored.")
            data[key] = int(time.time())
        elif type_hint == "str":
            data[key] = generate_str_value(generation_rule)
        elif type_hint == "int":
            data[key] = generate_int_value(generation_rule)
        else:
            raise ValueError(f"Unsupported type '{type_hint}' for key '{key}'")

    return data

def generate_str_value(rule):
    if rule == "rand":
        return str(uuid.uuid4())
    elif rule.startswith("[") and rule.endswith("]"):
        rule = rule.replace("'", "\"")
        values = json.loads(rule)
        return random.choice(values)
    else:
        return rule

def generate_int_value(rule):
    if rule == "rand":
        return random.randint(0, 10000)
    elif rule.startswith("rand(") and rule.endswith(")"):
        range_str = rule[5:-1]
        try:
            start, end = map(int, range_str.split(","))
            return random.randint(start, end)
        except ValueError:
            raise ValueError(f"Invalid range format in rule '{rule}'")
    elif rule.startswith("[") and rule.endswith("]"):
        rule = rule.replace("'", "\"")
        values = json.loads(rule)
        return random.choice(values)
    elif rule == "":
        return None
    else:
        try:
            return int(rule)
        except ValueError:
            raise ValueError(f"Cannot convert '{rule}' to int")



def validate_schema(schema_str):
    try:
        schema = json.loads(schema_str)

        jsonschema.Draft7Validator.check_schema(schema)
        return 2
    except json.JSONDecodeError:

        if os.path.exists(schema_str):
            try:
                with open(schema_str, "r") as f:
                    schema = json.load(f)
                jsonschema.Draft7Validator.check_schema(schema)
                return 1
            except (json.JSONDecodeError, jsonschema.exceptions.SchemaError) as e:
                print(f"Invalid schema in file: {e}")
                return 0
        else:
            print("Invalid JSON format.")
            return 0
    except jsonschema.exceptions.SchemaError as e:
        print(f"Invalid schema: {e.message}")
        return 0

def handle_schema(schema: str) -> str:
    schema_type = validate_schema(schema)
    if schema_type == 1:
        with open(schema, "r") as f:
            result = f.read()
            return result
    elif schema_type == 2:
        return schema
    else:
        return ""
    
def generate_json(schema):
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

schema_str = '{"date":"timestamp:", "name": "str:rand", "type":"str:[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}'
#print(parse_schema(schema_str))