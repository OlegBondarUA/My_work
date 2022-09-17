import math
import multiprocessing
import concurrent.futures

from requests import get
from time import time
from pprint import pprint


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


def create_list_subreddits(url):
    data = get(url).json()
    list_subreddits = []
    for i in data['data']:
        list_subreddits.append((i['subreddit'], ))
    print(' 1 function')
    return list_subreddits


def create_subreddit_request(subreddit):
    subreddit_request = {}
    request = f'https://api.pushshift.io/reddit/comment/' \
              f'search?subreddit={subreddit[0]}'
    subreddit_request[subreddit] = request
    print('2 function')
    return subreddit_request


def collect(subreddit_request):
    subreddit_response = {}
    for key, value in subreddit_request.items():
        subreddit_response[key[0]] = get(value).json()
    print('3 function')
    return subreddit_response


def create_result(subreddit_response):
    comments_by_subreddit = {}
    for subreddit, response in subreddit_response.items():
        comment_by_author = {}
        for post in response['data']:
            author = post.get('author')
            comment = post.get('body')
            if author in comment_by_author.keys():
                comment_by_author[author].append(comment)
            else:
                comment_by_author[author] = [comment]
        comments_by_subreddit[subreddit] = comment_by_author
    print('4 function')
    return comments_by_subreddit


def process(qu):
    subreddit = qu.get()
    subreddit_request = create_subreddit_request(subreddit)
    subreddit_response = collect(subreddit_request)
    comments_by_subreddit = create_result(subreddit_response)
    print('5 function')
    qu.put(comments_by_subreddit)


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
########################################################
    full_list = []

    url = 'https://api.pushshift.io/reddit/comment/search'

    list_subreddits = create_list_subreddits(url)

    queue = multiprocessing.Queue()
    processes = []
    for subreddit in list_subreddits[:5]:
        queue.put(subreddit)
        p = multiprocessing.Process(target=process, args=(queue,))
        p.start()
        processes.append(p)

    [p.join() for p in processes]
    # print(queue.empty())

    while not queue.empty():
        full_list.append(queue.get())

    pprint(full_list)


if __name__ == '__main__':
    main()
