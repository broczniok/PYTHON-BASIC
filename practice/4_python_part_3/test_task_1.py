import pytest
from datetime import datetime
from task_1 import WrongFormatException
from freezegun import freeze_time
import task_1


@pytest.mark.freeze_time
def test_calculate_days_2():
    with freeze_time('2024-05-26'):
        current_date = '2024-05-26'
        assert task_1.calculate_days(current_date) == 0

    with freeze_time('2024-05-27'):
        current_date_plus_1 = '2024-05-26'
        assert task_1.calculate_days(current_date_plus_1) == 1

    with freeze_time('2024-05-25'):
        current_date_minus_1 = '2024-05-26'
        assert task_1.calculate_days(current_date_minus_1) == -1



def test_calculate_days_exceptions():
    with pytest.raises(WrongFormatException):
        task_1.calculate_days('26-05-2024')
        assert task_1.calculate_days('26-05-2024') == None

