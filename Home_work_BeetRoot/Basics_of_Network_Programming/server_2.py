import socket

SERVER = '127.0.0.1'
PORT = 8017
HEADER = 1024

msgFromServer = 'Hello UDP Client'

bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((SERVER, PORT))

print('UDP server up and listening')

while True:
    bytesAddressPair = UDPServerSocket.recvfrom(HEADER)

    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    clientMsg = 'Message from Client:{}'.format(message)
    clientIP = 'Client IP Address:{}'.format(address)

    print(clientMsg)
    print(clientIP)

    UDPServerSocket.sendto(bytesToSend, address)
