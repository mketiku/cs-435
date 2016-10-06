#!/usr/bin/env python3

import socket


''' Simple client for a http get request.'''
__author__ = "Michael Ketiku"
__project__ = "http_request_client"
___email__ = "mketiku@gmail.com"
___date__ = "09-29-16"
___status__ = "stable"
#create an INET, STREA
Ming socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'www.google.com'
port = 80

server = socket.gethostbyname(host)

# now connect server on the specified port
s.connect((host, port))

#Send some data to host
message = "GET / HTTP/1.1\r\n\r\n"
s.sendall(bytes(message, 'UTF-8'))

# receive and print 4096 B of response
response = s.recv(4096)

print("Received: {}".format(response.decode('UTF-8')))

# signal our intent to close the socket and then close it
# the shutdown step is _essentially_ optional
s.shutdown(socket.SHUT_RDWR)
s.close()
