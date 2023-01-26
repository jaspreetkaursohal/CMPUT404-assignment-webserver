#  coding: utf-8 
import socketserver
from pathlib import Path
from email.utils import formatdate

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
    
    def check_path_existance(self, path):
        return path.exists()
    def check_method_name(self,request_info):
        if(len(request_info) > 0):
                method_name = request_info.split()
                return(method_name[0])
        else:
            pass
    
    def get_url(self,request_info):
        if(len(request_info) > 1):
                method_name = request_info.split()
                return(method_name[1])

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        decoded_value = self.data.decode('utf-8')
        if(self.check_method_name(decoded_value)=='GET'):
            url = self.get_url(decoded_value)
            url = "www" + url
            url_path = Path(url)
            if(self.check_path_existance(url_path)):
                if(url[-4:] == ".css" ):
                    f = open(url_path, 'r')
                    val = f.read()
                    return_ans = "HTTP/1.1 200 OK\r\n"
                    return_ans += "Content-Type: text/{}; charset=utf-8\r\n".format(url[-3:])
                elif(url[-5:] == ".html"):
                    f = open(url_path, 'r')
                    val = f.read()
                    return_ans = "HTTP/1.1 200 OK\r\n"
                    return_ans += "Content-Type: text/{}; charset=utf-8\r\n".format(url[-4:])
                elif(url[-1] == '/'):
                    url += "index.html"
                    url_path = Path(url)
                    f = open(url_path, 'r')
                    val = f.read()
                    return_ans = "HTTP/1.1 200 OK\r\n"
                    return_ans += "Content-Type: text/html; charset=utf-8\r\n"
                elif url[-1] != '/':
                    url2 =  url + '/index.html'
                    url_path = Path(url)
                    url_path2 = Path(url2)
                    if(self.check_path_existance(url_path2) == False):
                        return_ans = "HTTP/1.1 404 Not Found\r\n" 
                        val = ""
                    else:
                        f = open(url_path2, 'r')
                        val = f.read()
                        return_ans = "HTTP/1.1 301 Moved Permanently\r\n" 
                        return_ans += "Content-Type: text/html; charset=utf-8\r\n"
                        return_ans += "Location:http://127.0.0.1:8080{}/\r\n".format(self.get_url(decoded_value))
            else:
                
                return_ans = "HTTP/1.1 404 Not Found\r\n\r\n"
                val = ""
        else:
            return_ans = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            val=""
        return_ans += "Date:{}\r\n".format(formatdate(timeval=None, localtime=False, usegmt=True))
        return_ans += "Content-Length: {}\r\n".format(len(val))
        return_ans += "\r\n"
        return_ans += val
        self.request.sendall(return_ans.encode())



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()