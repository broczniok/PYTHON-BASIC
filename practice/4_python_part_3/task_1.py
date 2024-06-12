"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from datetime import datetime

class WrongFormatException(Exception):
    pass


def calculate_days(from_date: str) -> int:
    try:
        current_date = datetime.today()
        date_format = '%Y-%m-%d'
        given_date = datetime.strptime(from_date, date_format)
        t = (current_date - given_date).days 
        return t

    except ValueError:
        raise WrongFormatException()
    except TypeError:
        raise WrongFormatException()


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""
