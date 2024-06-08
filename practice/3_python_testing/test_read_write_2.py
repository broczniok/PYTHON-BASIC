"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '2_python_part_2'))

import importlib

res = importlib.import_module('task_read_write_2')


def test_generate_words(n=20):
    assert res.generate_words()
    assert len(res.generate_words()) == 20


def test_write_to_file_utf(tmp_path):
    d = tmp_path / "test_utf"
    d.mkdir()

    res.write_to_file_utf(d)

    assert len(list(tmp_path.iterdir())) == 1

    files = list(d.iterdir())

    with files[0].open(encoding="UTF-8") as f:
        lines = f.readlines()

    assert len(lines) == len(res.generate_words())
    for line in lines:
        assert isinstance(line, str)


def test_write_to_file_cp1252(tmp_path):
    d = tmp_path / "test_cp1252"
    d.mkdir()

    res.write_to_file_cp1252(d)

    assert len(list(tmp_path.iterdir())) == 1

    files = list(d.iterdir())
    with files[0].open(encoding="CP1252") as f:
        lines = f.read()

        assert ',' in lines

