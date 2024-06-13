import _csv
import os
from random import randint

import csv
import concurrent.futures
import random

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        f0, f1 = 0, 1
        for _ in range(2, n + 1):
            f0, f1 = f1, f0 + f1
        return f1

def write_fib_to_file(n):
    fib_value = fib(n)
    file_path = os.path.join(OUTPUT_DIR, f'{n}.csv')
    with open(file_path, 'w') as f:
        f.write(str(fib_value))

def func1(array: list):
    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(write_fib_to_file, array)

def read_fib_from_file(file_path):
    with open(file_path, 'r') as f:
        fib_value = f.read().strip()
        if os.path.splitext(os.path.basename(file_path))[0] != 'result':
            ordinal = int(os.path.splitext(os.path.basename(file_path))[0])
            return (ordinal, fib_value)

def func2(result_file: str):
    file_paths = [os.path.join(OUTPUT_DIR, fname) for fname in os.listdir(OUTPUT_DIR) if fname.endswith('.csv')]

    with concurrent.futures.ThreadPoolExecutor() as ex:
        fib_values = list(ex.map(read_fib_from_file, file_paths))


    with open(result_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        try:
            csv_writer.writerows(fib_values)
        except _csv.Error:
            csv_writer.writerows("")

if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    func1(array=[random.randint(1000, 5000) for _ in range(1000)])
    func2(result_file=RESULT_FILE)