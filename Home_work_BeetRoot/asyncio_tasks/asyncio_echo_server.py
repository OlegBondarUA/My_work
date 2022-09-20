import asyncio
import socket
from asyncio import AbstractEventLoop

PORT = 8004
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)


# AbstractEventLoop надає базовий контракт для циклів подій.
async def echo(connection: socket, loop: AbstractEventLoop):
    try:
        # Цикл, який постійно очікує даних від підключення клієнта
        while massage := await loop.sock_recv(connection, 1024):
            # Отримавши дані, надішліть їх тому клієнту
            await loop.sock_sendall(connection, massage)
    except Exception as error:
        print(error)


# AbstractEventLoop надає базовий контракт для циклів подій.
async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        # сокет встановлений у неблокуючий режим.
        connection.setblocking(False)
        print(f'Got a connection from {address}')
        # Щоразу, коли ми отримуємо з’єднання, створюйте ехо-завдання
        # для прослуховування даних клієнта.
        asyncio.create_task(echo(connection, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER, PORT)

    # сокет встановлений у неблокуючий режим.
    server_socket.setblocking(False)

    # зв'язування сокета з серверною адресою.
    server_socket.bind(server_address)

    server_socket.listen()
    print(f'Server {SERVER} start')
    # Запустіть співпрограму, щоб прослухати підключення.
    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())
