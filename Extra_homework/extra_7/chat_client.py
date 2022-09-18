import socket
import threading
import time

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = '25.41.62.153'
PORT = 8771
CLIENT.connect((ADDRESS, PORT))

# ADDRESS = input('IP-адрес входу:')

while True:
    nick_name = input('type your nick name: (up to 10 characters)')
    if 1 < len(nick_name) < 10:
        break


print('Connected')
print('type "Exit" to leave')


def massage_time():
    current_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", current_time)
    return current_time


def out_massage():
    while True:
        massage = input('')
        if massage == 'exit':
            CLIENT.close()
            break
        if CLIENT:
            CLIENT.send(f'\n{massage_time()} |'
                        f' {nick_name}: {massage}'.encode('utf-8'))
            print(f'{massage_time()} | {nick_name}: {massage}')


def in_massage():
    while True:
        try:
            massage = CLIENT.recv(1024)
            massage = massage.decode('utf-8')
            if massage == 'exit':
                CLIENT.close()
                break
            print(massage)
        except OSError as error:
            print(error)
            break


tread_1 = threading.Thread(target=in_massage, name='input')
tread_2 = threading.Thread(target=out_massage, name='out')

tread_1.start()
tread_2.start()

tread_1.join()
tread_2.join()
