import unittest
from unittest.mock import Mock, patch
from task_5 import make_request
import urllib.request


class TestMakeRequest(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_make_request_success(self, mock_urlopen):
        
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b'success'

        mock_urlopen.return_value = mock_response
        
        status_code, body = make_request('https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock')
       
        self.assertEqual(status_code, 200)
        self.assertEqual(body, 'success')


if __name__ == '__main__':
    unittest.main()