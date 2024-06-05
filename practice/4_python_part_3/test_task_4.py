import unittest
from unittest.mock import Mock, patch
from task_4 import print_name_address, get_parser
from argparse import Namespace

class TestPrintNameAddress(unittest.TestCase):
    @patch('task_4.Faker')
    def test_print_name_address(self, faker_mock):
        
        m_1 = Mock()
        m_2 = Mock()
        m_3 = Mock()
        m_1.number = 2
        m_2.number = 2
        m_3.number = 2

        m_1.fields = ['name=name', 'address=address']
        m_2.fields = ['country=country', 'latitude=latitude']
        m_3.fields = ['url=url', 'email=email']

        
        fake_instance_1 = faker_mock.return_value
        fake_instance_1.name.return_value = 'John Doe'
        fake_instance_1.address.return_value = '123 Main St'

        fake_instance_2 = faker_mock.return_value
        fake_instance_2.country.return_value = 'Mayotte'
        fake_instance_2.latitude.return_value = 51.7514185

        fake_instance_3 = faker_mock.return_value
        fake_instance_3.url.return_value = 'http://fischer.info/'
        fake_instance_3.email.return_value = 'ybanks@example.com'
        
        print_name_address(m_1)
        print_name_address(m_2)
        print_name_address(m_3)
        
        fake_instance_1.name.assert_called_with()
        fake_instance_1.address.assert_called_with()

        fake_instance_2.country.assert_called_with()
        fake_instance_2.latitude.assert_called_with()

        fake_instance_3.url.assert_called_with()
        fake_instance_3.email.assert_called_with()


if __name__ == '__main__':
    unittest.main()
