import pytest
import os
import tempfile
import threading
import json
import shutil
from script import validate_schema, process_schema, get_parser, generate_int_value, generate_str_value


@pytest.fixture
def temp_json_file():
    schema = {
        'date': "timestamp:",
        "name": "str:rand",
        "type": ['client', 'partner', 'government'],
        "age": "int:rand(1, 90)"
    }
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as f:
        json.dump(schema, f)
        temp_filename = f.name
    yield temp_filename
    os.remove(temp_filename)

@pytest.mark.parametrize("data_type, rule, expected_type", [
    ("str", "rand", str),
    ("int", "rand(1, 100)", int),
    ("list", "['a', 'b', 'c']", str),
])
def test_generate_values(data_type, rule, expected_type):
    if data_type == "str":
        assert isinstance(generate_str_value(rule), expected_type)
    elif data_type == "int":
        assert isinstance(generate_int_value(rule), expected_type)
    elif data_type == "list":
        assert isinstance(generate_str_value(rule), expected_type)

@pytest.mark.parametrize("schema_str, is_valid", [
    ('{"date": "timestamp:", "name": "str:rand", "type": "[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}', True),
    ('{"date": "timestamp:", "name": "str:rand", "type": "invalid", "age": "int:rand(1, 90)"}', False),
])
def test_validate_schema(schema_str, is_valid):
    if is_valid:
        assert validate_schema(schema_str) in [1, 2]
    else:
        with pytest.raises(SystemExit):
            validate_schema(schema_str)

def test_process_schema_with_temp_json_file(temp_json_file, temp_directory):
    process_schema(temp_json_file, temp_directory, 1, "testfile", 10, "count", 0, threading.Lock())
    assert len(os.listdir(temp_directory)) == 1

@pytest.fixture
def temp_directory():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)

def test_clear_path_action(temp_directory):
    filename = os.path.join(temp_directory, "testfile_1.json")
    with open(filename, 'w') as f:
        f.write('{"test": "data"}')

    parsed_args = get_parser()
    parsed_args.path_to_save_files = temp_directory
    parsed_args.data_schema = '{"date": "timestamp:"}'
    parsed_args.clear_path = True

    assert parsed_args.path_to_save_files == temp_directory
    assert parsed_args.clear_path is True

def test_file_saving(temp_directory):
    schema_str = '{"date": "timestamp:", "name": "str:rand"}'
    process_schema(schema_str, temp_directory, 1, "testfile", 10, "count", 0, threading.Lock())
    assert len(os.listdir(temp_directory)) == 1

def test_multiprocessing_file_creation(temp_directory):
    schema_str = '{"date": "timestamp:", "name": "str:rand"}'
    process_schema(schema_str, temp_directory, 3, "testfile", 10, "count", 0, threading.Lock())
    assert len(os.listdir(temp_directory)) == 3

if __name__ == "__main__":
    pytest.main()
