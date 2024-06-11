"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context

def make_request(url: str) -> Tuple[int, str]:
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
        status_code = resp.getcode()
        body = resp.read().decode('utf-8')
        return (status_code, body)
    except Exception as e:
        print(e)
        return (0, str(e))


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
