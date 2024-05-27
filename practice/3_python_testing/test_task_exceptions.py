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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_part_2')))
import task_exceptions 

# def foo():
#     print("Hello World")

# def test_foo(capfd):
#     foo()
#     out, err = capfd.readouterr()
#     assert out == "Hello World\n"

def test_division_ok(capfd):
     task_exceptions.division(2,2)
     out, err = capfd.readouterr()
     assert out == '1.0\n'


def test_division_by_zero(capfd):
     task_exceptions.division(1,0)
     out, err = capfd.readouterr()
     assert out == "Division by zero\n"
     assert err == ''



def test_division_by_one(capfd):
    with pytest.raises(task_exceptions.DivisionByOneException) as exc_info:
        task_exceptions.division(1, 1)
    assert str(exc_info.value) == 'Deletion on 1 get the same result'  
    out, err = capfd.readouterr()
    assert out.strip() == ''
    assert err.strip() == ''
