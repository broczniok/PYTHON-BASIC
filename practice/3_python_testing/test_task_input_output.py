"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '2_python_part_2'))

import importlib
res = importlib.import_module('task_input_output')


def test_read_numbers_without_text_input(capfd):
    with patch.object(sys, 'argv', ['task_input_output.py', '1', '2', '3', '4', '1']):
            res.read_numbers(5)
            out,err = capfd.readouterr()
            assert out == 'Avg: 2.2\n'


def test_read_numbers_with_text_input(capfd):
    with patch.object(sys, 'argv', ['task_input_output.py', 'fasfas', 'sda', 'Text', 'asdad', 'dass']):
            res.read_numbers(5)
            out,err = capfd.readouterr()
            assert out == 'No numbers entered\n'
