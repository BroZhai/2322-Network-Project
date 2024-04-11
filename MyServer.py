import socket
import threading
import os
from datetime import datetime
#from flask import Flask,send_file //不能用 :(

# Server configuration

Request_Counter=1
WEB_ROOT = 'D:\\Python\\2322Project\\rootFolder'
LOG_FILE = 'D:\\Python\\2322Project\\server_log.txt'  # Log file path

# HTTP response status codes
OK200_STATUS = '200 OK'
NOT404_STATUS = '404 Not Found'
BAD400_STATUS = '400 Bad Request'
NMD304_STATUS = '304 Not Modified'

#处理客户端Socket的请求
def handle_request(Csocket, Caddress):
    global Request_Counter
    # Receive the HTTP request from the client
    request = Csocket.recv(1024).decode()

    #Extract the ip and port from the tupple
    ClientIP=Caddress[0]
    ClientPort=Caddress[1]
    
    #Output section within the console
    print('Request',Request_Counter,'from',ClientIP,':',ClientPort)
    print(request)
    Request_Counter+=1

    headers=request.split('\n'); #通过'\n'对request进行分割
    filename=headers[0].split()[1]; #取得对应的"路由请求段"

    if filename=="/":
        respond="HTTP/1.1 400 Bad Request\n\n<h1>You're trying to access the default root, there is nothing but a BAD REQUEST here :|</h1> \n if you want to access the index page, click <a href=\"index.html\">here</a> :)  (This access record has been stored inside the server_log.txt file [within the same directory])"
        log_request(Caddress, "[ROOT]", BAD400_STATUS)
        Csocket.sendall(respond.encode())
        Csocket.close()
        return
    else:
        # User did send a path for requesting
        filepath = os.path.join(WEB_ROOT, filename.lstrip('/'))
        # Check whether the requested file exists or not
        if not os.path.isfile(filepath): #文件不存在，返回404响应信息给客户端，并记录到log文件中
            respond="HTTP/1.1 404 NOT FOUND\n\n<h1>404 Error: Sorry, the route (file) you are accessing is not exist :(</h1> \n (This access record has been stored inside the server_log.txt file [within the same directory])"
            Csocket.sendall(respond.encode())
            # send_response(Csocket, NOT404_STATUS, 'The file is not found :(')
            log_request(Caddress, filename, NOT404_STATUS)
            Csocket.close()
            return
            

        # return the image files.
        # if filename=="/images/test.jpg":
        #     last_modified=datetime(2024,4,11) #defined a last_modified date for the source file
        #     with open(filepath, 'rb') as file:
        #         if 'If-Modified-Since' in request:
        #             splited_lines = request.split('\r\n')
        #             for line in splited_lines:
        #                 if line.startswith('If-Modified-Since:'):
        #                     modified_str = line.split(':')[1].strip() #Extract the date from the Client's request
        #                     break
        #             if_modifiedTime = datetime.strptime(modified_str, '%a, %d %b %Y %H:%M:%S %Z')
        #             if if_modifiedTime >= last_modified:
        #                 # 构建304 Not Modified响应
        #                 response = 'HTTP/1.1 304 Not Modified\r\n\r\n'
        #                 log_request(Caddress,filename,NMD304_STATUS)
        #                 Csocket.send(response.encode())
        #         image=file.read()
        #         respond="HTTP/1.1 200 OK\n\n"
        #         respond+="Content-Type: image/jpeg\r\n"
        #         respond+="Last-Modified: {}\r\n\r\n".format(last_modified.strftime('%a, %d %b %Y %H:%M:%S %Z'))
        #         Csocket.sendall(respond.encode()+image)
        #         log_request(Caddress, filename, OK200_STATUS)
        #         Csocket.close()
        if filename.startswith("/images"):
            last_modified=datetime(2022,4,11) #defined a last_modified date for the source file
            with open(filepath, 'rb') as file:
                if 'If-Modified-Since' in request:
                    splited_lines = request.split('\r\n')
                    for lines in splited_lines:
                        if lines.startswith('If-Modified-Since:'):
                            modified_str = lines.split(':')[1].strip() #Extract the date from the Client's request
                            break
                    if_modifiedTime = datetime.strptime(modified_str, '%a, %d %b %Y %H:%M:%S %Z')
                    if if_modifiedTime >= last_modified:
                        image=file.read()
                        respond="HTTP/1.1 304 Not Modified\n\n"
                        Csocket.sendall(respond.encode()+image)
                        log_request(Caddress, filename, NMD304_STATUS)
                        Csocket.close()
                    else:
                        image=file.read()
                        respond="HTTP/1.1 200 OK\n\n"
                        Csocket.sendall(respond.encode()+image)
                        log_request(Caddress, filename, OK200_STATUS)
                        Csocket.close()
                else:
                    image=file.read()
                    respond="HTTP/1.1 200 OK\n\n"
                    Csocket.sendall(respond.encode()+image)
                    log_request(Caddress, filename, OK200_STATUS)
                    Csocket.close()
        else:
            with open(filepath, 'rb') as file:
                file_content = file.read()
                respond="HTTP/1.1 200 OK\n\n"+file_content.decode()+"<h5>You have successfully reached the contents above.</h5> <p>(This access record has been stored inside the server_log.txt file [within the same directory])</p>"
                Csocket.sendall(respond.encode())
                log_request(Caddress, filename, OK200_STATUS)
                Csocket.close()
                # if 'If-Modified-Since' in request:
                #     splited_lines = request.split('\r\n')
                #     for line in splited_lines:
                #         if line.startswith('If-Modified-Since:'):
                #             modified_str = line.split(':')[1].strip()  # 从客户端请求中提取日期
                #             break
                #     if_modifiedTime = datetime.strptime(modified_str, '%a, %d %b %Y %H:%M:%S %Z')
                #     if if_modifiedTime >= last_modified:
                #         # 构建304 Not Modified响应
                #         log_request(Caddress, filename, NMD304_STATUS)
        #         image = file.read()
        #         respond = "HTTP/1.1 200 OK\n\n"
        #         respond += "Content-Type: image/jpeg\r\n"   
        #         #respond += "Last-Modified: {}\r\n\r\n".format(last_modified.strftime('%a, %d %b %Y %H:%M:%S %Z'))
        #         Csocket.sendall(respond.encode() + image)
        #         log_request(Caddress, filename, OK200_STATUS)
        #         Csocket.close()
        # else:
        #     with open(filepath, 'rb') as file:
        #         file_content = file.read()
        #         respond="HTTP/1.1 200 OK\n\n"+file_content.decode()+"<h5>You have successfully reached the contents above.</h5> <p>(This access record has been stored inside the server_log.txt file [within the same directory])</p>"
        #         Csocket.sendall(respond.encode())
        #         log_request(Caddress, filename, OK200_STATUS)   
        # Send the HTTP response to the client
        # send_response(Csocket, OK200_STATUS, file_content) 
        # Log the request
            
    # try:
    #     #访问(打开)本地存储的index.html
    #     htmlFile=open('D:\Python\lab5 HTTP网络编程'+filename)
    #     content=htmlFile.read(); #复制(读取)文件内容到本地变量中
    #     htmlFile.close();#关闭读取文件，好习惯

    #     ##模拟HTTP响应
    #     respond="HTTP/1.1 200 OK\n\n<h1>You are HTTP 200 OK feline baka</h1>"+content ##回应消息
        
    # except FileNotFoundError:
    #     respond="HTTP/1.1 400 Not Found\n\n<h1>AHah, that can not be reached...</h1>"
    # Csocket.sendall(respond.encode())


    

#给客户端回应的 "响应信息" (未使用，可无视)
def send_response(Csocket, status_code, content):
    # Generate the current date and time for the HTTP header

    #取得系统时间
    current_time = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')

    # Construct a HTTP response message
    response = f'HTTP/1.1 {status_code}\r\n'
    response += f'Date: {current_time}\r\n'
    response += 'Server: SimpleWebServer\r\n'
    response += 'Connection: close\r\n'
    response += 'Content-Type: text/html\r\n'  # Assuming all files are HTML
    response += f'Content-Length: {len(content)}\r\n'
    response += '\r\n'
    # response += content.decode()

    # Send the response to the client
    Csocket.sendall(response.encode())

#记录请求到log文件的函数
def log_request(Caddress, filename, status_code):
    # Generate the current date and time for the log entry
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Format the log entry
    log_entry = f'{Caddress[0]}:{Caddress[1]} - [{current_time}] "{filename}" {status_code}'

    # Write the log entry to the log file
    try:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry + '\n')
    except IOError as e:
        print("Exception encountered when write to the log file! ")

def start_server():
    #Create the socket for server
    Ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Ssocket.bind(("127.0.0.1", 8080)) #Default using 127.0.0.1:8080

    # Listen for incoming connections
    Ssocket.listen(5)
    print('Server is now listening on 127.0.0.1:8080 ')

    while True:
        # Accept a client connection
        Csocket, Caddress = Ssocket.accept()

        #创建线程，这里指定进入了handle_request()函数，同时将参数用args传递了 handle_request()
        ClinetThread = threading.Thread(target=handle_request, args=(Csocket, Caddress)) 
        ClinetThread.start()

if __name__ == '__main__':
    start_server() ##Launch the server