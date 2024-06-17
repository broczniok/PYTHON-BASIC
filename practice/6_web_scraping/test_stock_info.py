from stock_info import make_request, get_soup
import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup


class TestFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_make_request_success(self, mock_get):
        mock = Mock()
        mock.status_code = 200
        mock.content = b'content'
        mock_get.return_value = mock

        status, content = make_request('https://www.google.com/')
        self.assertEqual(status, 200)
        self.assertEqual(content, b'content')

    @patch('requests.get')
    def test_make_request_failure(self, mock_get):
        mock = Mock()
        mock.status_code = 404
        mock_get.return_value = mock

        result = make_request('https://www.google.com/')
        self.assertIsNone(result[1])

    @patch('stock_info.make_request')
    def test_get_soup(self, mock_make_request):
        mock_make_request.return_value = (200, b'<html></html>')

        soup = get_soup('https://www.google.com/')
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(str(soup), '<html></html>')


if __name__ == '__main__':
    unittest.main()
