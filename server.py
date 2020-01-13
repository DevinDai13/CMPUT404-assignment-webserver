#  coding: utf-8 
import socketserver
from pathlib import Path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        method = self.data.splitlines()[0].decode().split(" ")[0]
        sendBack = ""
        header = "\r\n\r\n"

        if method == " ":
            print("Error: Can not determine request method!")    
        elif method == 'GET':
            file = self.data.splitlines()[0].decode().split(" ")[1]
            html301 = "<!DOCTYPE html><html><body>301 Moved Permanently</body><p>Redirected to %s/</p></html>"%file
            html404 = "<!DOCTYPE html><html><body>404 Not Found</body></html>"
            display = ""
            pathCheck = 0
            fileExtension = ""
            directoryPath = "www/" + file

            if Path(directoryPath).is_file():
                open(directoryPath).read()
                fileExtension = directoryPath.split(".")[1].lower()
                pathCheck = 1
            elif not Path(directoryPath).is_file() and Path(directoryPath).is_dir():
                pathEnding = directoryPath[-1]
                if pathEnding != "/":
                    display = html301
                    pathCheck = 0
                elif pathEnding == "/":
                    directoryPath = "www/"+file+"/index.html"   
                    if Path(directoryPath).is_file():          
                        fileExtension = directoryPath.split(".")[1].lower()
                        pathCheck = 1
                    else:
                        pathCheck = 0
            else:
                pathCheck = 0

            if pathCheck == 1 and fileExtension == "html":
                sendBack = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "Connection: alive" + header + open(directoryPath).read()         
            elif pathCheck == 1 and fileExtension == "css":
                sendBack = "HTTP/1.1 200 OK\n" + "Content-Type: text/css\n" + "Connection: alive" + header + open(directoryPath).read()
            elif pathCheck == 0 and display == html301:
                sendBack = "HTTP/1.1 301 Permanently moved\r\n" + "Content-Type: html\n" + "Connection: close" + header + html301
            else:
                sendBack = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: html\n" + "Connection: close" + header + html404
        else:
            html405 = "<!DOCTYPE html><html><body>405 Method Not Allowed</body></html>"
            sendBack = "HTTP/1.1 405 Method Not Allowed\r\n" + "Content-Type: html\n" + "\n" + "Connection: close" + header + html405
        
        self.request.sendall(bytearray(sendBack,'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()