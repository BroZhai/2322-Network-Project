# 2322-Network-Project
#### 孩子们，我回来了 :)
一个用Python socket实现的小服务器，也是这个课的project

This program has used socket for HTTP Server Programing
ps: the "rootFolder" is the root of the server where all the requested resources are stored in it.

**Must do!!** 
To use this program, firstly you need to setup the configurations at the start of the "MyServer.py" by modifing the the "WEB_ROOT"(Server Folder) and another path for the expoerted "LOG_FILE" in Line 10 and 11 in the source file.
[Rememeber to add a additional filename for the log file in its path (e.g. \server_log.txt) ]


*Optional Setup* 
You can change the server address and port in Line 15 and 16 in the source file.

**>> Instructions** 
After the configuration above, you can now start the "MyServer.py" and access the server in your browser
[The default address is 127.0.0.1:8080]

If you want to test the "If-Modified-Since" section. You'll see other 2 python files namely the "Cache_Outdated_Client (200 OK)" and "Not_Outdated_Client (304 Not Modified)". You can just directly run these 2 programs to check the log file later on. [Please do remember your execute sequence]

Once you are finished, a "server_log.txt" file will be generated within the same folder, where you can find all the logs you had request to the server and the response codes.

//End of readme 