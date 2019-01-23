#  coding: utf-8 
import socketserver
import os

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
    
    base = open("www/index.html").read()
    basecss = open("www/base.css").read()
    deep = open("www/deep/index.html").read()
    deepcss = open("www/deep/deep.css").read()


    def handle(self):
        self.data = self.request.recv(1024).strip()
        # Decode these bytes into workable information
        data = self.data.decode("utf-8")

        # Determine the type and location of the request
        # We are going to assume that the type of the request and host are
        # always the first two elements in this data object
        # data[0].split() = [type, location, httpVersion]
        # data[1].split() = [host, ]
        # Im not sure we even need the host right now
        data = data.splitlines()
        data = data[0].split()[1]
        
        # Now we have the path, and we can determine what page to serve the user
        # We can also serve 404 if that page does not exist
        # We could probably hardcode this functionality for this assignment as well
        # So that is what we will do

        # Base page
        if data == "/index.html" or data == "/" or data == "/index.html/" or data == "/base.css":
            self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/css;\r\n", 'utf-8'))
            self.request.sendall(bytearray(self.basecss, 'utf-8'))
            self.request.sendall(bytearray("Content-Type: text/html;\r\n", 'utf-8'))
            self.request.sendall(bytearray(self.base,'utf-8'))
            
            return

        # Deep page
        if data == "/deep" or data == "/deep/" or data == "/deep/index.html" or data == "/deep/base.css":
            self.request.sendall(bytearray("HTTP/1.1 200 OK",'utf-8'))
            self.request.sendall(bytearray(self.deepcss,'utf-8'))
            self.request.sendall(bytearray(self.deep,'utf-8'))
            return

        else:
            # print(data, "Page not found")
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            # We could return some random page not found html stuff here
            return



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
