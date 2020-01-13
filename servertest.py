import socketserver
from pathlib import Path

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        method = self.data.splitlines()[0].decode().split(" ")[0]
        
        sendBack = "Unidentified"

        if method == " ":
            print("Error: Can not determine request method!")
            pass
        
        elif method == 'GET':
            file_path = self.data.splitlines()[0].decode().split(" ")[1]

            pathCheck, file, directoryPath = self.pathCheck(file_path)

            fileExtension = directoryPath.split(".")[1].lower()

            if pathCheck and fileExtension == "html":
                sendBack = "HTTP/1.1 200 OK\n" + "Content-Type: text/html\n" + "Connection: alive" + "\r\n\r\n" + open(directoryPath).read()
            
            elif pathCheck and fileExtension == "css":
                sendBack = "HTTP/1.1 200 OK\n" + "Content-Type: text/css\n" + "Connection: alive" + "\r\n\r\n" + open(directoryPath).read()

            elif directoryPath == "www/301.html":
                sendBack = "HTTP/1.1 301 Permanently moved\r\n" + "Content-Type: html\n" + "Connection: close" + "\r\n\r\n" + open(directoryPath).read()

            else:
                sendBack = "HTTP/1.1 404 Not Found\r\n" + "Content-Type: html\n" + "Connection: close" + "\r\n\r\n" + open(directoryPath).read()

        else:
            directoryPath = "www/405.html"
            sendBack = "HTTP/1.1 405 Method Not Allowed\r\n" + "Content-Type: html\n" + "\n" + "Connection: close" + "\r\n\r\n" + open(directoryPath).read()
        
        self.request.sendall(bytearray(sendBack,'utf-8'))

    def pathCheck(self, file_path):
        try:
            directoryPath = "www" + file_path
            file = open(directoryPath).read()
            return True, file, directoryPath

        except Exception as ex:
            exception_type = type(ex).__name__
            end_character = directoryPath[-1]
            if exception_type == "IsADirectoryError":
                if end_character != "/":
                    file = "<!DOCTYPE html> <html><body>301 Moved Permanently<br/> Location: %s/ <br/></body></html>"%file_path
                    directoryPath = "www/301.html"
                    return False, file, directoryPath

                elif end_character == "/":
                    directoryPath = "www"+file_path+"index.html"
                    try:
                        file = open(directoryPath).read()
                        return True, file, directoryPath

                    except:
                        directoryPath = "www/404.html"
                        file = open(directoryPath).read()
                        return False, file, directoryPath

            else:
                directoryPath = "www/404.html"
                file = open(directoryPath).read()
                return False, file, directoryPath

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
