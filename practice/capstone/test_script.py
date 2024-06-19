import pytest
import os
import tempfile
import threading
import json
import shutil
from script import validate_schema, process_schema, get_parser, generate_int_value, generate_str_value, process_schema_item


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


def test_validate_schema():
    valid_schema_str = '{"date": "timestamp:", "name": "str:rand", "type": "[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}'
    assert validate_schema(valid_schema_str) in [1, 2]

    invalid_schema_str = "{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",age\": \"int:rand(1, 90)\"}"

    with pytest.raises(SystemExit) as excinfo:
        validate_schema(invalid_schema_str)
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 1


def test_process_schema_with_temp_json_file(temp_json_file, temp_directory):
    with open(temp_json_file, "r") as r:
        temp_json_file = r.read()
    process_schema(temp_json_file, temp_directory, 1, "testfile", 10, "count", 0, threading.Lock(),1)
    assert len(os.listdir(temp_directory)) == 1


@pytest.fixture
def temp_directory():
    dirpath = tempfile.mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


def test_clear_path_called(monkeypatch, temp_directory):
    # Set up arguments including --clear_path
    args = [
        "script.py",
        "--path_to_save_files", temp_directory,
        "--data_schema", '{"date": "timestamp:", "name": "str:rand", "type": "[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}',
        "--files_count", "2",
        "--file_name", "file",
        "--clear_path"
    ]

    monkeypatch.setattr("sys.argv", args)

    get_parser()
    get_parser()

    assert len(os.listdir(temp_directory)) == 2, "Files were not cleared as expected"


def test_clear_path_not_called(monkeypatch, temp_directory):
    args = [
        "script.py",
        "--path_to_save_files", temp_directory,
        "--files_count", "2",
        "--file_name", "file",
        "--data_schema", '{"date": "timestamp:", "name": "str:rand", "type": "[\'client\', \'partner\', \'government\']", "age": "int:rand(1, 90)"}'
    ]

    monkeypatch.setattr("sys.argv", args)

    get_parser()
    get_parser()


    assert len(os.listdir(temp_directory)) == 2*2


def test_file_saving(temp_directory):
    schema_str = '{"date": "timestamp:", "name": "str:rand"}'
    process_schema(schema_str, temp_directory, 1, "testfile", 10, "count", 0, threading.Lock(),1)
    assert len(os.listdir(temp_directory)) == 1


def test_multiprocessing_file_creation(temp_directory):
    schema_str = '{"date": "timestamp:", "name": "str:rand"}'
    process_schema(schema_str, temp_directory, 3, "testfile", 10, "count", 0, threading.Lock(),1)
    assert len(os.listdir(temp_directory)) == 3


def test_timestamp():
    key, value = process_schema_item("date", "timestamp:")
    assert key == "date"
    assert isinstance(value, int)


def test_str_value():
    key, value = process_schema_item("name", "str:John Doe")
    assert key == "name"
    assert value == "John Doe"


def test_int_value():
    with pytest.raises(SystemExit) as er:
        key, value = process_schema_item("age", "int:20-30")
        assert key == "age"
        assert er.value.code == 1

def test_wrong_expression_timestamp():
    with pytest.raises(SystemExit):
        process_schema_item("date", "timestamp:rand(5)")

def test_wrong_expression_str():
    with pytest.raises(SystemExit):
        process_schema_item("name", "str:rand(5)")

def test_wrong_data_type():
    with pytest.raises(SystemExit):
        process_schema_item("unknown", "unknown:random")

def test_missing_colon():
    with pytest.raises(SystemExit):
        process_schema_item("name", "John Doe")

if __name__ == "__main__":
    pytest.main()
