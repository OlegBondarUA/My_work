import requests
import datetime
import json
from pprint import pprint


# task 01

response = requests.get("https://wikipedia.org/robots.txt")
test = response.text


###############################################################################

# task 02

response = requests.get('https://api.pushshift.io/reddit/comment/search/')
file = response.json()
# pprint(file)


def get_comment(item):
    return item['body']


comments = map(get_comment, file['data'])
comment = []
for i in comments:
    data = {'comment': i}
    comment.append(data)


###############################################################################

# task 03

open_weather_token = '6b5e304be9e747c2293c99ce1941d06f'


def get_weather(city, open_weather_toke):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Хмарно \U00002601',
        'Rain': 'Дощ \U00002614',
        'Drizzle': 'Дощ \U00002614',
        'Thunderstorm': 'Сніг \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        request = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}'
            f'&appid={open_weather_toke}&units=metric'
        )
        data = request.json()
        # pprint(data)

        city = data['name']
        cur_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Глянь у вікно, не розумію що там за погода!'
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = \
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = \
            datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = \
            datetime.datetime.fromtimestamp(data['sys']['sunset']) -\
            datetime.datetime.fromtimestamp(data['sys']['sunrise'])

        print(f'###{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}###\n'
              f'Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n'
              f'Вологість: {humidity}%\nТиск: {pressure} мм.рт.ст\n'
              f'Вітер: {wind} м/с\nСхід сонця: {sunrise_timestamp}\n'
              f'Захід сонця: {sunset_timestamp}\n'
              f'Тривалість дня: {length_of_the_day}\n'
              f'Гарного дня!')
    except Exception as ex:
        print(ex)
        print('Перевірте назву міста')


def main():
    # task 01
    with open('robots.xtx', '+w') as file:
        file.write(test)

    # task 02

    with open('comment.json', 'w') as file_1:
        json.dump(comment, file_1, indent=4)

    # task 03
    city = input('Введіть місто: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
