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

def read_numbers(n: int) -> None:
    numbers = []
    sum = 0

    for i in range(n):
        user_input = input(f"Enter number {i+1}: ")
        if user_input.isdigit():
            numbers.append(int(user_input))

    if len(numbers) > 0:
        for number in numbers:
            sum += number
        print('Avg:', sum / len(numbers))
    else:
        print("No numbers entered")

read_numbers(5)

my line