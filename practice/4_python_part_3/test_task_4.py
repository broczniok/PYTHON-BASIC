import unittest
from unittest.mock import Mock, patch
from task_4 import print_name_address, get_parser
from argparse import Namespace

class TestPrintNameAddress(unittest.TestCase):
    @patch('task_4.Faker')
    def test_print_name_address(self, faker_mock):
        
        m = Mock()
        m.number = 2
        m.fields = ['name=name', 'address=address']

        
        fake_instance = faker_mock.return_value
        fake_instance.name.return_value = 'John Doe'
        fake_instance.address.return_value = '123 Main St'

        
        print_name_address(m)

        
        fake_instance.name.assert_called_with()
        fake_instance.address.assert_called_with()


if __name__ == '__main__':
    unittest.main()
