import argparse
import sys
import jsonschema
import uuid
import time
import logging
import json
import os
import random
import threading
from configparser import ConfigParser
import ast

class JsonSchemaException(Exception):
    pass

class ThreadingException(Exception):
    pass

def fill_parser(config, args):
    result = {
        "pathfile": [args.path_to_save_files],
        "files_count": [args.files_count or int(config["DEFAULT"]["files_count"])],
        "file_name": [args.file_name or str(config["DEFAULT"]["file_name"])],
        "data_schema": [args.data_schema],
        "data_lines": [args.data_lines or int(config["DEFAULT"]["data_lines"])],
        "clear_path": [args.clear_path or str(config["DEFAULT"]["clear_path"])],
        "file_prefix": [args.file_prefix or str(config["DEFAULT"]["file_prefix"])],
        "multiprocessing": [args.multiprocessing or int(config["DEFAULT"]["multiprocessing"])]
    }
    return result


def get_parser():

    config = ConfigParser()
    try:
        config.read("default.ini")
    except:
        print("default.ini file reading went wrong")
        sys.exit(1)

    parser = argparse.ArgumentParser(prog="magicgenerator", description="Capstone Project function that generates fake JSON files from command line.")
    parser.add_argument('--path_to_save_files', metavar="pathfile",required=True, help="Where all files need to be saved", type=str)
    parser.add_argument('--files_count', metavar="file_count",  help="How much json files to generate", type=int)
    parser.add_argument('--file_name', metavar="file_name", help="What should the files be named (base: file_name)", type=str)
    parser.add_argument('--file_prefix', metavar="file_prefix", help="What prefix for file name to use if there is more than 1 file to generate", type=str)
    parser.add_argument('--data_schema', metavar="data_schema", required=True, help="It should be string with json schema, could be loaded as path to json file with schema or schema entered to command line", type=str)
    parser.add_argument('--data_lines', metavar="data_lines", help="Count of lines for each file (base=1000)", type=int)
    parser.add_argument('--clear_path', metavar="clear_path", help="Use if you want to overwrite all other files with same name in chosen directory")
    parser.add_argument('--multiprocessing', metavar="multiprocessing", help="The number of processes used to create files (base=1)", type=int)

    args = parser.parse_args()

    arguments = fill_parser(config, args)

    #print("pathfile:",arguments["pathfile"][0])
    #print("files count:",arguments["files_count"][0])
    #print("file name:",arguments["file_name"][0])
    print("data schema:", str(arguments["data_schema"][0]), type(arguments["data_schema"][0]))
    #print("data lines:",arguments["data_lines"][0])
    #print("clear path:",arguments["clear_path"][0])
    #print("file prefix", arguments["file_prefix"][0])
    #print("multiprocessing", arguments["multiprocessing"][0])

    schema_str = args.data_schema

    print("Schema od 0",schema_str[0])
    if schema_str.startswith("{"):
        print("Starts with {")


    schema_validation_result = validate_schema(schema_str)

    if arguments["multiprocessing"][0] < 0:
        sys.exit(1)

    if arguments["multiprocessing"][0] > os.cpu_count():
        arguments["multiprocessing"][0] = os.cpu_count()

    if schema_validation_result == 0:
        print("Invalid schema")
        return
    else:
        threads = []
        for i in range(arguments["multiprocessing"][0]):
            thread = threading.Thread(target=process_schema, args=(schema_str, arguments["pathfile"][0],arguments["file_count"][0], arguments["file_name"][0], arguments["data_lines"][0], arguments["clear_path"][0], arguments["file_prefix"][0], i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

'''
    if schema_validation_result == 0:
        print("Invalid schema")
        return
    elif schema_validation_result == 2:
        print("Schema loaded from file and validated.")
        print(parse_schema(schema_str,2))
        print("^^^^ to powyzej jest z pliku^^^^^")
    elif schema_validation_result == 1:
        print("Schema string validated.")
        print(parse_schema(schema_str, 1))
        print("^^^^ to powyzej jest ze stringa^^^^^")

'''







def process_schema(schema_str, pathfile , file_count, file_name, data_lines, clear_path, file_prefix, source):
    if validate_schema(schema_str) == 0:
        print("Invalid schema")
        return
    elif validate_schema(schema_str) == 2: # Schema is from file
        print("Schema loaded from file and validated.")
        print(parse_schema(schema_str,2))
        print("^^^^ to powyzej jest z pliku^^^^^")
    elif validate_schema(schema_str) == 1: # Schema is from string
        print("Schema string validated.")
        print(parse_schema(schema_str, 1))
        print("^^^^ to powyzej jest ze stringa^^^^^")


def parse_schema(schema_str, type):
    if type == 2:
        with open(schema_str, "r") as r:
            schema = json.load(r)

    elif type == 1:
        schema = json.loads(schema_str)
    else:
        sys.exit(1)

    data = {}

    for key, value in schema.items():
        if isinstance(value, list):
            data[key] = random.choice(value)
        elif ":" in value:
            type_hint, generation_rule = value.split(":", 1)
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
        else:
            data[key] = random.choice(ast.literal_eval(value))

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
    if os.path.exists(schema_str):
        try:
            with open(schema_str, "r") as f:
                schema = json.load(f)

                if isinstance(schema, dict) and 'type' in schema and schema['type'] == ['client', 'partner', 'government']:
                    schema['type'] = ["string", "array"]
                    schema['items'] = {"type": "string"}
                    schema['minItems'] = 1
                    schema['uniqueItems'] = True
                jsonschema.Draft7Validator.check_schema(schema)
                print("Done")
            return 2
        except (json.JSONDecodeError, jsonschema.exceptions.SchemaError) as e:
            print(f"Invalid schema in file: {e}")
            return 0, None
    else:
        try:
            schema = json.loads(schema_str)

            schema['type'] = ["string", "array"]
            schema['items'] = {"type": "string"}
            schema['minItems'] = 1
            schema['uniqueItems'] = True

            jsonschema.Draft7Validator.check_schema(schema)
            return 1
        except (json.JSONDecodeError, jsonschema.exceptions.SchemaError) as e:
            print(f"Invalid schema string: {e}")
            return 0



get_parser()

schema_str = "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"
