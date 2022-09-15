import concurrent.futures
import math

from time import time


NUMBERS = [
   2,  # prime
   1099726899285419,
   1570341764013157,  # prime
   1637027521802551,  # prime
   1880450821379411,  # prime
   1893530391196711,  # prime
   2447109360961063,  # prime
   3,  # prime
   2772290760589219,  # prime
   3033700317376073,  # prime
   4350190374376723,
   4350190491008389,  # prime
   4350190491008390,
   4350222956688319,
   2447120421950803,
   5,  # prime
]


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True
###############################################################################


def main():

    # task 01

    t1 = time()
######################################################
    # Time spent to function 23.30

    # for n in NUMBERS:
    #     print(is_prime(n))
######################################################
    # Time spent to function 7.83

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(NUMBERS, executor.map(is_prime, NUMBERS)):
            print('%d is prime: %s' % (number, prime))

    print(f'Time spent to function {time() - t1:.2f}')
#######################################################
    # Time spent to function 23.95

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for number, prime in zip(NUMBERS, executor.map(is_prime, NUMBERS)):
    #         print('%d is prime: %s' % (number, prime))
    #
    # print(f'Time spent to function {time() - t1:.2f}')


if __name__ == '__main__':
    main()
