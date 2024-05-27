"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import pytest
import os
import sys
from datetime import datetime, timedelta
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../python_part_2')))
from task_classes import Teacher, Student, Homework

@pytest.fixture
def teacher():
    return Teacher('Dmitry', 'Orlyakov')

@pytest.fixture
def student():
    return Student('Vladislav', 'Popov')

@pytest.fixture
def homework1():
    return Homework('Learn functions', 0)

@pytest.fixture
def homework2():
    return Homework('create 2 simple classes', 5)

@pytest.fixture
def homework3():
    return Homework('create 2 simple classes', -5)


def test_creating_teacher(teacher):
    assert teacher.first_name == 'Dmitry'
    assert teacher.last_name == 'Orlyakov'

def test_creating_student(student):
    assert student.first_name == 'Vladislav'
    assert student.last_name == 'Popov'

def test_creating_homework1(homework1):
    assert homework1.text == 'Learn functions'
    assert homework1.created.date() == datetime.now().date()
    assert homework1.deadline == timedelta(days=0)

def test_creating_homework2(homework2):
    assert homework2.text == 'create 2 simple classes'
    assert homework2.created.date() == datetime.now().date()
    assert homework2.deadline == timedelta(days=5)

def test_creating_homework3():
    with pytest.raises(ValueError, match="Days cannot be negative"):
        Homework('Invalid homework', -1)
    

def test_create_homework(teacher):
    homework = teacher.create_homework("Test task", 3)
    assert homework.text == "Test task"
    assert isinstance(homework.created, datetime)
    assert homework.deadline == timedelta(days=3)

def test_student_do_homework(student,homework1,homework2): #By checking this method we know that is_active() method works as well
    assert student.do_homework(homework1) == None
    assert student.do_homework(homework2) == homework2




