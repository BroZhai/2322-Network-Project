from socket import *

clientSocket=socket(AF_INET,SOCK_STREAM) # Create a client socket object
print("Client Socket Create Successfully")

Port=8080; 
clientSocket.connect(('127.0.0.1',Port)); # Connect the client socket to the Server
request_headers = [
    'GET /images/test.jpg HTTP/1.1',
    'Host: localhost',
    'If-Modified-Since: Mon, 11 Apr 1970 12 00 00 UTC', # Outdated Cache (smaller the date 11th April 1997 on the server)
    'Connection: close',
    '\r\n'
]
request = '\r\n'.join(request_headers)
clientSocket.sendall(request.encode()) # The Server would respond 200 OK

respondBuffer=clientSocket.recv(2048).decode()
print("response from server: ",respondBuffer)

clientSocket.close() #Close the test client connection