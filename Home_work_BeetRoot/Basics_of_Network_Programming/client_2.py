import socket

msgFromClient = 'Hello UDP Server'
bytesToSend = str.encode(msgFromClient)

SERVER = '127.0.0.1'
PORT = 8017
HEADER = 1024

ADDRESS = (SERVER, PORT)

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(bytesToSend, ADDRESS)
msgFromServer = UDPClientSocket.recvfrom(HEADER)
msg = "Message from Server {}".format(msgFromServer[0])

print(msg)
