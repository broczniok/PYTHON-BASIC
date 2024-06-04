"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""
import argparse
from faker import Faker


def print_name_address(args: argparse.Namespace) -> None:
    fake = Faker()
    instances = []
    for _ in range(args.number):
        instance = {}
        for field in args.fields:
            if '=' in field:
                key, provider = field.split('=')
                instance[key] = getattr(fake, provider)()
        instances.append(instance)
    for instance in instances:
        print(instance)
        


def get_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    parser.add_argument('--fields', nargs='+')
    
    known_args, unknown_args = parser.parse_known_args()
    fields = []
    for arg in unknown_args:
        if arg.startswith('--'):
            field = arg[2:]
            fields.append(field)
    setattr(known_args, 'fields', fields)
    return known_args


if __name__ == '__main__':
    print_name_address(get_parser())













