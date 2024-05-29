import pytest
from task_2 import OperationNotFoundException, math_calculate

@pytest.mark.parametrize("test_input, args, expected", [
    ('log', [1024, 2], 10.0), 
    ('ceil', [10.7], 11)
])
def test_math_calculate(test_input, args, expected):
    assert math_calculate(test_input, *args) == expected

def test_math_calculate_exceptions():
    with pytest.raises(OperationNotFoundException):
        math_calculate('akjsfnakf', 2)

