"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '2_python_part_2'))

import importlib
res = importlib.import_module('task_exceptions')

def test_division_ok(capfd):
    result = res.division(2, 2)
    out, err = capfd.readouterr()
    assert result == 1.0
    assert out == "Division finished\n"

def test_division_by_zero(capfd):
    result = res.division(1, 0)
    out, err = capfd.readouterr()
    assert result is None
    assert out == "Division by zero\nDivision finished\n"
    assert err == ''

def test_division_by_one(capfd):
    with pytest.raises(res.DivisionByOneException) as exc_info:
        res.division(1, 1)
    assert str(exc_info.value) == "Deletion on 1 get the same result"
    out, err = capfd.readouterr()
    assert out == "Division finished\n"
    assert err == ''