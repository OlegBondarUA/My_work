import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# host = input('IP-адрес входу:')
host = 'tuskotrushs-MacBook-Pro.local'

while True:
    name = input('Введіть свій нікнейм, не більше 10 символів та не меньше 1: ')
    if 1 < len(name) < 10:
        break

port = 8777

client.connect((host, port))

print('Ви підключилися до серверу')
print('exit, щоб покинути сервер')


def out_datas():
    while True:
        out_data = input('')
        print()
        if out_data == 'exit':
            break
        client.send(f'{name}:{out_data}'.encode('utf-8'))
        print('%s:%s', (name, out_data))


def in_datas():
    while True:
        in_data = client.recv(1024)
        print(in_data.decode('utf-8'))


t1 = threading.Thread(target=in_datas, name='input')
t2 = threading.Thread(target=out_datas, name='out')

t1.start()
t2.start()

t1.join()
t2.join()

