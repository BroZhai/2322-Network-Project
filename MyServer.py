import socket
import threading
import os
from datetime import datetime

# Server configuration
Request_Counter=1

## Change the directory here
WEB_ROOT = r'D:\Python\2322Project\rootFolder' # Define the path for "Server Folder" (location)
LOG_FILE = r'D:\Python\2322Project\server_log.txt'  # Define the path for the exported Log file 
# (do remember to add the filename for the log file. e.g: \server_log.txt)

# Setup the server address and opening here
Server_IP="127.0.0.1"
Server_Port=8080

# Define HTTP response status codes
OK200_STATUS = '200 OK'
NOT404_STATUS = '404 Not Found'
BAD400_STATUS = '400 Bad Request'
NMD304_STATUS = '304 Not Modified'

def start_server():
    #Create the socket for server
    Ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Ssocket.bind((Server_IP, Server_Port)) #Default using 127.0.0.1:8080 [Defined above]

    # Limit the incoming connections
    Ssocket.listen(5)
    print("Server is now listening on",Server_IP,":",Server_Port)

    while True:
        # Accept a client connection
        Csocket, Caddress = Ssocket.accept()

        # Create multiple threads using the threading library for handling the requests.
        ClinetThread = threading.Thread(target=handle_request, args=(Csocket, Caddress)) 
        ClinetThread.start()

#Handle the request coming from the client socket
#(will be used in the thread (start_server))
def handle_request(Csocket, Caddress):
    global Request_Counter ## a Counter is used to record and indicate the requests
    # Receive the HTTP request from the client
    request = Csocket.recv(1024).decode()

    #Extract the ip and port from the tupple
    Client_IP=Caddress[0]
    Client_Port=Caddress[1]
    
    #Output section within the console
    print('Request',Request_Counter,'from',Client_IP,':',Client_Port)
    print(request)
    Request_Counter+=1

    headers=request.split('\n'); #Split the request into different parts using '\n'
    filename=headers[0].split()[1]; #Gain the "filename(route)" in the splited headers

    if filename=="/": # generate a bad request while accesing the default route ('/')
        respond="HTTP/1.1 400 Bad Request\n\n<h1>You're trying to access the default root, there is nothing but a 400 BAD REQUEST here :|</h1> \n if you want to access the index page, click <a href=\"index.html\">here</a> :)  <p>\n (This access record has been stored inside the server_log.txt file [within the same directory])</p>"
        log_request(Caddress, "[ROOT]", BAD400_STATUS)
        Csocket.sendall(respond.encode())
        Csocket.close()
        return
    else: 
        # Extract the "filename(route)" and joint with the defined "Server Path", to form the absolute path  
        filepath = os.path.join(WEB_ROOT, filename.lstrip('/'))

        # Check whether the requested file exists or not within the combined absolute path
        if not os.path.isfile(filepath):
            # Requested File(s) are not founded, respond 404 to client and store the record in the log file
            respond="HTTP/1.1 404 NOT FOUND\n\n<h1>404 Error: Sorry, the route (file) you are accessing does not exist :(</h1> \n (This access record has been stored inside the server_log.txt file [within the same directory])"
            Csocket.sendall(respond.encode())
            log_request(Caddress, filename, NOT404_STATUS)
            Csocket.close()
            return

        #The requested file does exist in the Server, try to retreive the file
           
        # if the file requested is a image, it needs to be separately handled
        if filename.startswith("/images"):
            last_modified=datetime(1997,4,11) #defined a last_modified date for the source file
            with open(filepath, 'rb') as file:
                if 'If-Modified-Since' in request:
                    splited_lines = request.split('\r\n')
                    for lines in splited_lines:
                        if lines.startswith('If-Modified-Since:'):
                            modified_str = lines.split(':')[1].strip() #Extract the date from the Client's request
                            break
                    
                    #Client's request of "Modified time"
                    if_modifiedTime = datetime.strptime(modified_str, '%a, %d %b %Y %H %M %S %Z')
                    #If the cache of client's side isn't outdated, return 304 Not Modified, else 200 OK
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
                connection_Type=""
                file_content = file.read()
                splited_lines = request.split('\r\n')
                for lines in splited_lines:
                    if lines.startswith('Connection:'):
                        connection_Type = lines.split(':')[1].strip() #Extract the date from the Client's request
                        break
                respond="HTTP/1.1 200 OK\n\n"+"\n\n"+file_content.decode()+"<h5>You have successfully reached the contents above.</h5> <p>(This access record has been stored inside the server_log.txt file [within the same directory])</p>"
                Csocket.sendall(respond.encode())
                Connection_msg="Connection Type acknowledged from server: "+connection_Type
                Csocket.sendall(Connection_msg.encode())
                log_request(Caddress, filename, OK200_STATUS)
                Csocket.close()

#Define a log function that write the log records to a specific file.

def log_request(Caddress, filename, status_code):
    # Get the time for each log entry
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Format the log entry
    log_entry = f'{Caddress[0]}:{Caddress[1]} - [{current_time}] "{filename}" {status_code}'

    # Write the log entry to the log file
    try:
        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry + '\n')
    except IOError as e: # prevent any writting permission and other issues
        print("Exception encountered when write to the log file! ")


start_server() #Launch the server