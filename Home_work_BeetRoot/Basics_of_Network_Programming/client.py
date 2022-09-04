import socket


PORT = 8002
SERVER = '127.0.0.1'
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'exit'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER, PORT))


def send(message):
    message = message.encode(FORMAT)
    message_length = len(message)
    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


while (message := input('Введіть повідомлення: ')) != DISCONNECT_MESSAGE:
    send(message)


