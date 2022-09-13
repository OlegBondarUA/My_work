import threading
import requests
import json


counter = 0
rounds = 100000


class Counter(threading.Thread):

    def run(self):
        global counter
        for _ in range(rounds):
            counter += 1
        return counter


class Counter2(threading.Thread):

    def run(self):
        global counter
        for _ in range(rounds):
            counter += 1
        return counter


def get_coment():
    response = requests.get('https://api.pushshift.io/reddit/comment/search/')
    data = response.json()

    name = data['data']
    comments = []
    for i in name:
        data = {
            'author': i['author'],
            'created': i['created_utc'],
            'body': i['body']
        }
        comments.append(data)
    with open('get_comments.json', 'a') as file:
        json.dump(comments, file, indent=4)


get_coment()


def main():
    count_1 = Counter()
    count_2 = Counter2()
    count_1.start()
    count_2.start()

    count_1.join()
    count_2.join()

    print(counter)

    # task 02

    get_coment()


if __name__ == '__main__':
    main()
