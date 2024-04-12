from socket import *
import os

clientSocket=socket(AF_INET,SOCK_STREAM)
print("Client Socket Create Successfully")

Port=8080; 
clientSocket.connect(('127.0.0.1',Port))
request_headers = [
    'GET /images/test.jpg HTTP/1.1',
    'Host: localhost',
    'If-Modified-Since: Mon, 11 Apr 2024 12 00 00 UTC',  # Cache that is fresh (Not outdated)
    'Connection: close',
    '\r\n'
]
request = '\r\n'.join(request_headers)
clientSocket.sendall(request.encode())

# The server should respond 304 Not Modified in this scenario

respondBuffer=clientSocket.recv(2048).decode()
print("response from server: ",respondBuffer)

clientSocket.close()