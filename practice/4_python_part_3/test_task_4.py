import argparse
import unittest
from io import StringIO
from unittest.mock import Mock, patch
from task_4 import print_name_address, get_parser


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

        print_test_args = argparse.Namespace(number=1, fields=['name=name', 'address=address', 'country=country'])

        with patch('sys.stdout', new=StringIO()) as fake_out:
            print_name_address(print_test_args)
            printed_output = fake_out.getvalue().strip()

        expected_output = (
            '{"name": "John Doe", "address": "123 Main St", "country": "Mayotte"}'
        )

        self.assertEqual(printed_output, expected_output)


class TestGetParser(unittest.TestCase):

    @patch('sys.argv', ['task_4.py', '2', '--fake-address=address', '--some_name=name'])
    def test_get_parser(self):
        expected = argparse.Namespace(number=2, fields=['fake-address=address', 'some_name=name'])
        result = get_parser()
        self.assertEqual(result.number, expected.number)
        self.assertEqual(result.fields, expected.fields)

    @patch('sys.argv', ['task_4.py', '5', '--city=city', '--state=state', '--zip=postcode'])
    def test_get_parser_multiple_fields(self):
        expected = argparse.Namespace(number=5, fields=['city=city', 'state=state', 'zip=postcode'])
        result = get_parser()
        self.assertEqual(result.number, expected.number)
        self.assertEqual(result.fields, expected.fields)

    @patch('sys.argv', ['task_4.py', '1', '--name=name'])
    def test_get_parser_single_field(self):
        expected = argparse.Namespace(number=1, fields=['name=name'])
        result = get_parser()
        self.assertEqual(result.number, expected.number)
        self.assertEqual(result.fields, expected.fields)



if __name__ == '__main__':
    unittest.main()
