"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import pytest

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_part_2')))
import task_read_write_2
import string

filepath = "/Users/broczniok/Desktop/PYTHON-BASIC/practice/python_part_2/files/"


def test_generate_words(n=20):
    assert task_read_write_2.generate_words()
    assert len(task_read_write_2.generate_words()) > 0

def test_write_to_file_utf(tmp_path):
    d = tmp_path / "test_utf"
    d.mkdir()

    task_read_write_2.write_to_file_utf(d)

    assert len(list(tmp_path.iterdir())) == 1

    files = list(d.iterdir())

    with files[0].open(encoding="UTF-8") as f:
        lines = f.readlines()

    for line in lines:
        assert line.strip().islower()
        assert all(c in string.ascii_lowercase for c in line.strip())

def test_write_to_file_cp1252(tmp_path):
    d = tmp_path / "test_cp1252"
    d.mkdir()

    task_read_write_2.write_to_file_cp1252(d)

    assert len(list(tmp_path.iterdir())) == 1

    files = list(d.iterdir())

    with files[0].open(encoding="CP1252") as f:
        content = f.read()

    words = content.split(',')

    for word in words:
        assert all(c in string.ascii_lowercase for c in word)

