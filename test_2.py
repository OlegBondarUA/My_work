import concurrent.futures
import requests
import multiprocessing

from pprint import pprint
from time import time


def create_subreddit(url):
    response = requests.get(url)
    data = response.json()
    subreddits = []
    for i in data['data']:
        subreddits.append(i['subreddit'])
    # print(subreddits)
    return subreddits


def create_subreddit_request(subreddits):
    response = {}
    for subreddit in subreddits:
        req = f'https://api.pushshift.io/reddit/comment/' \
              f'search?subreddit={subreddit}'
        response[subreddit] = req
    # print(request)
    return response


subreddit_response = {}


def _collect(subreddit, request):
    global subreddit_response
    data = requests.get(request)
    subreddit_response[subreddit] = data.json()
    return subreddit_response


def run_threads(subreddit_request):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for key, value in subreddit_request.items():
            executor.submit(_collect, key, value)


def run_multiprocessing(subreddit_request):
    for subreddit, request in subreddit_request.items():
        # print(subreddit)
        # print(request)
        with multiprocessing.Pool() as pool:
            pool.starmap(_collect, subreddit, request)


def create_result(subreddit_respons):
    comments_by_subreddit = {}
    for subreddit, response in subreddit_respons.items():
        comment_by_author = {}
        for post in response['data']:
            author = post['author']
            comment = post['body']
            if author in comment_by_author.keys():
                comment_by_author[author].append(comment)
            else:
                comment_by_author[author] = [comment]
        comments_by_subreddit[subreddit] = comment_by_author
    return comments_by_subreddit


def main():

    # task 01

    t1 = time()
######################################################
    # Time spent to function 23.30

    # for n in NUMBERS:
    #     print(is_prime(n))
######################################################
    # Time spent to function 7.83

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     for number, prime in zip(NUMBERS, executor.map(is_prime, NUMBERS)):
    #         print('%d is prime: %s' % (number, prime))
    #
    # print(f'Time spent to function {time() - t1:.2f}')
#######################################################
    # Time spent to function 23.95

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     for number, prime in zip(NUMBERS, executor.map(is_prime, NUMBERS)):
    #         print('%d is prime: %s' % (number, prime))
    #
    # print(f'Time spent to function {time() - t1:.2f}')

    # task 02

    url = 'https://api.pushshift.io/reddit/comment/search/'

    list_subreddit = create_subreddit(url)
    subreddit_request = create_subreddit_request(list_subreddit)
    # print(subreddit_request)

    # Time spent to function 6.65
    # run_threads(subreddit_request)

    run_multiprocessing(subreddit_request)
    result = create_result(subreddit_response)
    pprint(result)
    print(f'Time spent to function {time() - t1:.2f}')


if __name__ == '__main__':
    main()
