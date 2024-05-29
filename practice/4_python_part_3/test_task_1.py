import pytest
from datetime import datetime
import task_1
from task_1 import WrongFormatException

current_date = datetime(2024, 5, 27)

@pytest.mark.parametrize("test_input, expected", [
    ('2024-05-26', (current_date - datetime(2024, 5, 26)).days), 
    ('2024-05-28', (current_date - datetime(2024, 5, 28)).days),
    ('2024-05-27', 0)
])
def test_calculate_days(test_input, expected, mocker):
    mocker.patch('task_1.datetime')
    task_1.datetime.today.return_value = current_date
    task_1.datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)
    assert task_1.calculate_days(test_input) == expected

def test_calculate_days_exceptions():
    with pytest.raises(WrongFormatException):
        task_1.calculate_days('26-05-2024')

