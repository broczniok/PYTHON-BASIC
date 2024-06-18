#!/usr/bin/env python3
import argparse
import string
import sys
from math import ceil
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


def fill_parser(config, args):
    result = {
        "pathfile": [args.path_to_save_files],
        "files_count": [args.files_count or int(config["DEFAULT"]["files_count"])],
        "file_name": [args.file_name or str(config["DEFAULT"]["file_name"])],
        "data_schema": [args.data_schema],
        "data_lines": [args.data_lines or int(config["DEFAULT"]["data_lines"])],
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
        exit(1)

    parser = argparse.ArgumentParser(prog="magicgenerator",
                                     description="Capstone Project function that generates fake JSON files from command line.")
    parser.add_argument('--path_to_save_files', metavar="pathfile", required=True,
                        help="Where all files need to be saved", type=str)
    parser.add_argument('--files_count', metavar="file_count", help="How much json files to generate", type=int)
    parser.add_argument('--file_name', metavar="file_name", required=True, help="What should the files be named",
                        type=str)
    parser.add_argument('--file_prefix', choices=["count", "random", "uuid"],
                        help="What prefix for file name to use if there is more than 1 file to generate", type=str)
    parser.add_argument('--data_schema', metavar="data_schema", required=True,
                        help="It should be string with json schema, could be loaded as path to json file with schema or schema entered to command line",
                        type=str)
    parser.add_argument('--data_lines', metavar="data_lines", help="Count of lines for each file (base=1000)", type=int)
    parser.add_argument('--clear_path', action="store_false",
                        help="Use if you want to overwrite all other files with same name in chosen directory")
    parser.add_argument('--multiprocessing', metavar="multiprocessing",
                        help="The number of processes used to create files (base=1)", type=int)

    args = parser.parse_args()

    arguments = fill_parser(config, args)

    if os.path.isfile(arguments["pathfile"][0]):
        print("Used path is for file not directory")
        exit(1)
    elif arguments["pathfile"][0] == '.``':
        arguments["pathfile"][0] = str(os.getcwd())
    elif not os.path.exists(arguments["pathfile"][0]):
        os.makedirs(arguments["pathfile"][0])
        os.chmod(arguments["pathfile"][0], 0o777)

    if arguments["multiprocessing"][0] < 0:
        print("Invalid multiprocessing count.")
        exit(1)
    elif arguments["multiprocessing"][0] > os.cpu_count():
        arguments["multiprocessing"][0] = os.cpu_count()

    if arguments["files_count"][0] < 0:
        print("Invalid files count.")
        exit(1)
    elif arguments["files_count"][0] == 0: # Change it so it will instead be priting line = data_lines to console (do not write to file) and add multithreading to it
        print(parse_schema(str(arguments["data_schema"][0]),2))
        sys.exit(0)

    if validate_schema(str(arguments["data_schema"][0])) == 0:
        print("Invalid schema")
        exit(1)
    elif validate_schema(str(arguments["data_schema"][0])) == 1:
        print("Schema string validated")
    elif validate_schema(str(arguments["data_schema"][0])) == 2:
        print("Schema from file validated")

    if args.clear_path:
        for filename in os.listdir(arguments["pathfile"][0]):
            if arguments["file_name"][0] in filename:
                file_to_delete = os.path.join(arguments["pathfile"][0], filename)
                if os.path.isfile(file_to_delete):
                    os.remove(file_to_delete)

        print("Files deleted")

    schema_validation_result = validate_schema(str(arguments["data_schema"][0]))
    if schema_validation_result == 0:
        print("Invalid schema")
        exit(1)
    else:
        lock = threading.Lock()
        threads = []
        if arguments["multiprocessing"] > arguments["files_count"]:
            arguments["multiprocessing"] = arguments["files_count"]

        for i in range(arguments["multiprocessing"][0]):
            thread = threading.Thread(target=thread_task, args=(
                arguments["data_schema"][0],
                arguments["pathfile"][0],
                arguments["files_count"][0],
                arguments["file_name"][0],
                arguments["data_lines"][0],
                arguments["file_prefix"][0],
                i,
                arguments["multiprocessing"][0],
                lock
            ))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join(1)
            if thread.is_alive():
                print(f"Thread {thread.name} did not complete in time and will be terminated.")



def thread_task(schema_str, pathfile, files_count, file_name, data_lines, file_prefix, thread_index, total_threads,
                lock):
    files_per_thread = ceil(files_count / total_threads)
    start_index = thread_index * files_per_thread
    end_index = min(start_index + files_per_thread, files_count)

    process_schema(schema_str, pathfile, end_index - start_index, file_name, data_lines, file_prefix, thread_index,
                   lock)


def get_unique_filename(pathfile, file_name, file_prefix, extension="json"):
    if file_prefix == "count":
        index = 1
        filename = os.path.join(pathfile, f"{file_name}_({index}).{extension}")
        while os.path.exists(filename):
            filename = os.path.join(pathfile, f"{file_name}_({index}).{extension}")
            index += 1
        return filename
    elif file_prefix == "uuid":
        filename = os.path.join(pathfile, f"{file_name}_({uuid.uuid4()}).{extension}")
        while os.path.exists(filename):
            filename = os.path.join(pathfile, f"{file_name}_({uuid.uuid4()}).{extension}")
        return filename
    elif file_prefix == "random":
        filename = os.path.join(pathfile,
                                f"{file_name}_({''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))}).{extension}")
        while os.path.exists(filename):
            filename = os.path.join(pathfile,
                                    f"{file_name}_({''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))}).{extension}")
        return filename
    else:
        print("Wrong file_prefix")
        exit(1)


def process_schema(schema_str, pathfile, files_count, file_name, data_lines, file_prefix, thread_index, lock):
    if validate_schema(schema_str) == 2:  # Schema is from file
        with lock:
            for _ in range(0, files_count):
                filename = get_unique_filename(pathfile, file_name, file_prefix)
                with open(filename, 'w') as file:
                    for _ in range(data_lines):
                        file.write(str(parse_schema(schema_str, 2)))
                        file.write("\n")
    elif validate_schema(schema_str) == 1:  # Schema is from string
        with lock:
            for _ in range(0, files_count):
                filename = get_unique_filename(pathfile, file_name, file_prefix)
                with open(filename, 'w') as file:
                    for _ in range(data_lines):
                        try:
                            file.write((str(parse_schema(schema_str, 1))))
                            file.write("\n")
                        except ValueError:
                            print("Wrongly rand inserted")
                            exit(1)


def parse_schema(schema_str, type):
    if type == 2:
        with open(schema_str, "r") as r:
            schema = json.load(r)

    elif type == 1:
        schema = json.loads(schema_str)
    else:
        exit(1)

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
                data[key] = generate_int_value(generation_rule)
            elif type_hint == "int":
                data[key] = generate_str_value(generation_rule)
            else:
                print(f"Unsupported type '{type_hint}' for key '{key}'")
                exit(1)
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
            print(f"Invalid range format in rule '{rule}'")
            exit(1)
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
            print("Cannot generate integer values")
            exit(1)


def validate_schema(schema_str):
    if schema_str.endswith(".json") and os.path.exists(schema_str):
        try:
            with open(schema_str, "r") as f:
                schema = json.load(f)
                if isinstance(schema, dict) and 'type' in schema and isinstance(schema['type'],list):
                    schema['type'] = ["string", "array"]
                    schema['items'] = {"type": "string"}
                    schema['minItems'] = 1
                    schema['uniqueItems'] = True
                jsonschema.Draft7Validator.check_schema(schema)
            return 2
        except (json.JSONDecodeError, jsonschema.exceptions.SchemaError) as e:
            print(f"Invalid schema in file: {e}")
            exit(1)
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
            exit(1)


if __name__ == "__main__":
    get_parser()
