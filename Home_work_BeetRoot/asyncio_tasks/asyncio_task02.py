import asyncio
import json
import httpx

from time import time
from requests import get


def create_list_subreddits(url):
    data = get(url).json()
    list_subreddits = []
    for i in data['data']:
        list_subreddits.append(i['subreddit'])
    return list_subreddits


def create_subreddit_request(list_subreddits):
    list_subreddits_url = []
    for subreddit in list_subreddits:
        request = f'https://api.pushshift.io/reddit/comment/' \
                  f'search?subreddit={subreddit}'
        list_subreddits_url.append(request)
    return list_subreddits_url


async def create_result(url):
    list_comments = []
    try:
        async with httpx.AsyncClient() as session:
            data = await session.get(url)
            for item in data.json()['data']:
                comments = {
                    'author': item['author'],
                    'comment': item['body'],
                    'subreddit': item['subreddit'],
                    'created_utc': item['created_utc']
                }
                list_comments.append(comments)
    except Exception as error:
        print(error)

    with open('comments.json', 'a') as file:
        json.dump(list_comments, file, indent=4)


async def main():

    url = 'https://api.pushshift.io/reddit/comment/search'

    list_subreddits = create_list_subreddits(url)
    urls = create_subreddit_request(list_subreddits)

    tasks = []

    for url in urls:
        task = asyncio.create_task(create_result(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    start = time()

    asyncio.run(main())

    end_time = time()
    print(f'Getting comments finished in {end_time - start:.2f} seconds')
