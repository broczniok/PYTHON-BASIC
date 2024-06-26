import pytest
from task_2 import OperationNotFoundException, math_calculate, NoAttributeException

@pytest.mark.parametrize("test_input, args, expected", [
    ('log', [1024, 2], 10.0), 
    ('ceil', [10.7], 11)
])
def test_math_calculate(test_input, args, expected):
    assert math_calculate(test_input, *args) == expected

def test_math_calculate_exceptions():
    with pytest.raises(OperationNotFoundException) as ex:
        result = math_calculate('akjsfnakf', 2)
        assert result == None
        assert "OperationNotFoundException: module 'math' has no attribute" in ex
    with pytest.raises(NoAttributeException):
        math_calculate('sqrt', 'asdas')
        assert math_calculate('sqrt', 'asdas') == None
