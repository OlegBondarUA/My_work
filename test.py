import concurrent
import multiprocessing
import json
from requests import get


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


def process(subreddit):
    subreddit_request = create_subreddit_request(subreddit)
    subreddit_response = collect(subreddit_request)
    comments_by_subreddit = create_result(subreddit_response)
    print('5 function')
    return comments_by_subreddit


def main():

    url = 'https://api.pushshift.io/reddit/comment/search'

    list_subreddits = create_list_subreddits(url)

    # with multiprocessing.Pool() as pool:
    #     result = pool.map(process, list_subreddits)
    #     print(result)

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     result = executor.submit(process, list_subreddits)
    #     for i in result:
    #         print(i)

    processes = []
    for i in list_subreddits:
        p = multiprocessing.Process(target=process, args=i)
        processes.append(p)
        p.start()
        p.join()
    print(list(processes))


if __name__ == '__main__':
    main()