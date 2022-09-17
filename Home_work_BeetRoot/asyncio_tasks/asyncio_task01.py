import asyncio
import concurrent.futures

from time import time


# async def fibonacci(number):
#     if number == 0:
#         return 0
#     if number == 1:
#         return 1
#
#     result = await fibonacci(number - 2) + await fibonacci(number - 1)
#     return result
#
#
# async def factorial(n):
#     if n < 0:
#         return 'Factorial does not exist'
#     elif n == 0:
#         return 1
#     else:
#         return n * await factorial(n - 1)
#
#
# async def squares(n):
#     square = n * n
#     return square
#
#
# async def cube(n):
#     return n * n * n
#
#
# async def main():
#     start = time()
#
#     result = await asyncio.gather(
#         fibonacci(30),
#         fibonacci(35),
#         fibonacci(25),
#         fibonacci(40))
#     print('fibonacci', result)
#     result_1 = await asyncio.gather(
#         factorial(4),
#         factorial(7),
#         factorial(9),
#         factorial(6))
#     print('factorial', result_1)
#     result_2 = await asyncio.gather(
#         squares(4),
#         squares(7),
#         squares(9),
#         squares(6))
#     print('squares', result_2)
#     result_3 = await asyncio.gather(
#         cube(30),
#         cube(35),
#         cube(25),
#         cube(40))
#     print('cube', result_3)
#
#     end_time = time()
#     print(f'Function asyncio finished in {end_time - start:.2f} seconds')

# Function asyncio finished in 59.89 seconds


# asyncio.run(main())


def fibonacci1(number):
    if number == 0:
        return 0
    if number == 1:
        return 1

    result = fibonacci1(number - 2) + fibonacci1(number - 1)
    return result


def factorial1(n):
    if n < 0:
        return 'Factorial does not exist'
    elif n == 0:
        return 1
    else:
        return n * factorial1(n - 1)


def squares1(n):
    square = n * n
    return square


def cube1(n):
    return n * n * n


def main():
    start = time()
    n = [30, 35, 25, 40]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(n, executor.map(fibonacci1, n)):
            print('%d is fibonacci: %s' % (number, prime))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(n, executor.map(factorial1, n)):
            print('%d is factorial: %s' % (number, prime))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(n, executor.map(squares1, n)):
            print('%d is squares: %s' % (number, prime))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(n, executor.map(cube1, n)):
            print('%d is cube: %s' % (number, prime))

    end_time = time()
    print(f'Function multiprocess finished in {end_time - start:.2f} seconds')
# Function multiprocess finished in 35.12 seconds


if __name__ == '__main__':
    main()
