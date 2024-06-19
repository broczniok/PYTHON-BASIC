#!/usr/bin/env python3
import argparse
import string
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict


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
    parser.add_argument('--clear_path', action="store_true",
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

    if args.multiprocessing == 0:
        arguments["multiprocessing"][0] = 0
    elif arguments["multiprocessing"][0] < 0:
        print("Invalid multiprocessing count.")
        exit(1)
    elif arguments["multiprocessing"][0] > os.cpu_count():
        arguments["multiprocessing"][0] = os.cpu_count()

    if arguments["files_count"][0] < 0:
        print("Invalid files count.")
        exit(1)
    elif arguments["files_count"][0] == 0:
        arguments["multiprocessing"][0] = 1

    if os.path.isfile(arguments["data_schema"][0]):
        with open(arguments["data_schema"][0], "r") as r:
            arguments["data_schema"][0] = r.read()

    validate_schema(str(arguments["data_schema"][0]))

    if args.clear_path:
        for filename in os.listdir(arguments["pathfile"][0]):
            if arguments["file_name"][0] in filename:
                file_to_delete = os.path.join(arguments["pathfile"][0], filename)
                if os.path.isfile(file_to_delete):
                    os.remove(file_to_delete)

        print("Files deleted")

    lock = threading.Lock()
    threads = []

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
                       lock, files_count)


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


def process_schema(schema_str, pathfile, files_count, file_name, data_lines, file_prefix, thread_index, lock, check):
    result_str = ""
    for _ in range(data_lines):
        with lock:
            try:
                result_str += (str(parse_schema(schema_str))) + '\n'
            except ValueError:
                print("Wrongly rand inserted")
                exit(1)
    if files_count > 0:
        with lock:
            for _ in range(0, files_count):
                filename = get_unique_filename(pathfile, file_name, file_prefix)
                with open(filename, 'w') as file:
                    file.write(result_str)
    elif check == 0:
        print(result_str)


def create_table(string):
    input_list = ast.literal_eval(string)
    output_list = [f"{item}" for item in input_list]
    return output_list


def process_schema_item(key, value):
    if not isinstance(value, list) and value.startswith('[') and value.endswith(']'):
        value = list(create_table(value))

    if isinstance(value, list):
        return key, random.choice(value)
    elif ":" in value:
        type_hint, generation_rule = value.split(":", 1)
        if type_hint == "timestamp":
            if "rand(" in generation_rule:
                print("Wrong expression near 'timestamp'")
                exit(1)
            if generation_rule:
                logging.warning(f"Timestamp type does not support any values. Value for '{key}' will be ignored.")
            return key, int(time.time())
        elif type_hint == "str":
            if "rand(" in generation_rule:
                print("Wrong expression near 'str'")
                exit(1)
            return key, generate_str_value(generation_rule)
        elif type_hint == "int":
            return key, generate_int_value(generation_rule)
        else:
            print("Wrong data type")
            exit(1)
    else:
        print("There should be ':' in schema")
        exit(1)


def parse_schema(schema_str):
    try:
        schema = json.loads(schema_str, object_pairs_hook=OrderedDict)
    except Exception as ex:
        print("Couldn't load schema", ex)
        exit(1)

    data = OrderedDict()
    results = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_schema_item, key, value): key for key, value in schema.items()}
        for future in as_completed(futures):
            key = futures[future]
            try:
                result_key, result_value = future.result()
                results.append((result_key, result_value))
            except Exception as ex:
                print(f"Error processing {key}: {ex}")
                exit(1)

    for key in schema.keys():
        for result_key, result_value in results:
            if key == result_key:
                data[key] = result_value
                break

    return dict(data)


def generate_str_value(rule):
    if rule == "rand":
        return str(uuid.uuid4())
    elif rule.startswith("[") and rule.endswith("]"):
        rule = rule.replace("'", "\"")
        values = json.loads(rule)
        return random.choice(values)
    elif rule is None:
        return ""
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
    elif rule is None:
        return None
    else:
        try:
            return int(rule)
        except ValueError:
            print("Cannot parse to integer")
            exit(1)


def validate_schema(schema_str):
    try:
        schema = json.loads(schema_str)

        schema['type'] = ["string", "array"]
        schema['items'] = {"type": "string"}
        schema['minItems'] = 1
        schema['uniqueItems'] = True

        jsonschema.Draft7Validator.check_schema(schema)
        print("Schema validated")
        return 1
    except (json.JSONDecodeError, jsonschema.exceptions.SchemaError) as e:
        print(f"Invalid schema string: {e}")
        exit(1)


if __name__ == "__main__":
    get_parser()
