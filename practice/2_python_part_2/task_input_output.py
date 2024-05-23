"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which rounded to 2 places after the decimal
If it doesn't exists, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered

"""
import sys

def read_numbers(n: int) -> str:
    arguments = sys.argv[1:]
    numbers = []
    sum = 0
    for number in arguments:
        if(number.isdigit()):
            numbers.append(int(number))
    if(n > len(numbers)):
        n = len(numbers)
    if(len(numbers) > 0):
        for i in range(0,n):
            sum += numbers[i]
        print('Avg:', sum/n)
    elif(len(numbers) == 0):
        print("No numbers entered")

read_numbers(5)

