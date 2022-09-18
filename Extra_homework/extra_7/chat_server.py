import socket
import threading
import time

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS = socket.gethostbyname(socket.gethostname())
PORT = 8771
# print(ADDRESS)

SERVER.bind((ADDRESS, PORT))
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.listen(10)
print('type "Exit" to leave from server')

# список клієнтів
clients_socket = []
# клієнти, які створили потоки
clients_with_thread = []


def massage_time():
    current_time = time.localtime()
    current_time = time.strftime("%H:%M:%S", current_time)
    return current_time


def users_connection():
    while True:
        client, address = SERVER.accept()
        clients_socket.append(client)
        print(f'server ip: {address} | users connect count: '
              f'{len(clients_socket)}', end='')


def receive_massage(client):
    while True:
        # приймання від клієнта
        try:
            massage = client.recv(1024)
        except Exception:
            clients_socket.remove(client)
            clients_with_thread.remove(client)
            print(f'server disconnected | '
                  f'users connect count: {len(clients_socket)}')
            break
        print(massage.decode('utf-8'))
        for _client in clients_socket:
            # відправляю інформацію іншим клієнтам
            if _client is not client:
                _client.send(massage)


def out_massage():
    while True:
        print('')
        massage = input('')
        print()
        print(f'{massage_time()} | server: {massage}')
        for client in clients_socket:
            client.send(f'server: {massage}'.encode('utf-8'))


def in_massage():
    while True:
        for _client in clients_socket:
            if _client in clients_with_thread:
                continue
            thread = threading.Thread(target=receive_massage, args=(_client,))
            thread.start()
            clients_with_thread.append(_client)


tread_1 = threading.Thread(target=in_massage, name='input')
tread_1.start()

tread_2 = threading.Thread(target=out_massage, name='out')
tread_2.start()

tread_3 = threading.Thread(target=users_connection, name='accept')
tread_3.start()


tread_2.join()
