import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()

port = 8777
print(host)

server.bind((host, port))

server.listen(10)
print('Enter exit для виходу з сервера')

# список клієнтів
clients = list()
# клієнти, які створили потоки
end = list()


def accept():
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(f'сервер підключено через {addr}: кількість підключених клієнтів:'
              f' ----- {len(clients)}' + '-' * 5, end='')


def recv_data(client):
    while True:
        try:
            indata = client.recv(1024)
        except Exception:
            clients.remove(client)
            end.remove(client)
            print(f'Сервер відключено: кількість підключень: {len(clients)}')
            break
        print(indata.decode('utf-8'))
        for clien in clients:
            # відправляю інформацію іншим клієнтам
            if clien is not client:
                clien.send(indata)


def out_datas():
    while True:
        print('')
        out_data = input('')
        print()
        if out_data == 'exit':
            break
        print('відправ усім: % s' % out_data)
        for client in clients:
            client.send(f'Сервер: {out_data}'.encode('utf-8'))


def in_datas():
    while True:
        for clien in clients:
            if clien in end:
                continue
            index = threading.Thread(target=recv_data, args=(clien,))
            index.start()
            end.append(clien)


t1 = threading.Thread(target=in_datas, name='input')
t1.start()

t2 = threading.Thread(target=out_datas, name='out')
t2.start()

t3 = threading.Thread(target=accept, name='accept')
t3.start()

t1.join()
t2.join()

for client in clients:
    client.close()
print('Сервер відключено')
