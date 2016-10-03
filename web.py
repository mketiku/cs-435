#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''Application serves a simple web directory.'''
__author__ = "Michael Ketiku"
__project__ = "SimpleHttpServer"
___email__ = "mketiku@gmail.com"
___status__ = "final"

import datetime
import os
import socket
import sys

# datetime format
format = "%a, %d %b %Y %H:%M:%S %Z"

# we'll store html and other files in an html directory
wwwroot = "{}/www/".format(os.getcwd())

# dictionaries to look up valid content-types and response code messages
# referencing codes['200'] will renurn 'OK'

permitted_methods = {
    'GET'
}
response_codes = {
    '200': 'OK',
    '304': 'Not Modified',
    '404': 'Not Found',
    '405': 'Method Not Allowed'
}
permitted_types = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'application/x-javascript',
    'jpg': 'image/jpeg',
    'gif': 'image/gif',
    'png': 'image/png'
}

# response_header = ''
# response = ''


def parse_headers(request):
    """Return a dictionary in the form Header => Value for all headers in *request*."""
    headers = {}
    for line in request.split('\n')[1:]:
        # blank line separates headers from content
        if line == '\r':
            break
        header_line = line.partition(':')
        headers[header_line[0].lower()] = header_line[2].strip()
    return headers

def handle_request(request):
    """Disassemble the request and create a response message."""
    req = request.split("\n")[0]  # create a list of items from the first line of the message
    headers = parse_headers(request)  # create a dictionary of header/value pairs

    # use the items() method to iterate over keys and values in a dictionary
    # print('>  Request type:  {}'.format(req))

    for h, v in headers.items():
        print("{} => {}".format(h, v))

    if req !='':
        method = req.split(' ')[0]
        print(method)
        requested_file = req.split(' ')[1]
    else:
        method= 'GET'
        print(method)
        requested_file = '/'

    if requested_file.endswith('/'):
        requested_file = requested_file + 'index.html'
    # check HTTP method is allowed and, if not, create response

    # check for if-modified-since and respond if not modified

    # to read the datetime string in a request we can specify the formatting and create a datetime object
    # datetime.datetime.strptime(v, format)
    # response_header = today +

    # to get a datetime object for *right now*
    today = datetime.datetime.today()
    if method in permitted_methods:
        try:
            # requested_file = "index.html"
            filename = "{}{}".format(wwwroot, requested_file)
            if os.path.isfile(filename):
                print("HTTP/1.1 200 OK\n")
            # determine content-type (can also be done inline when creating a response message)

            # the pythonic way to open files ... will close files automatically
            with open(filename, mode='rb') as f:
                # read the file and append it to the response message
                # use 'f.read()' to read the file contents
                response = f.read()
        except IOError as e:
            # 404 response ... file not found
            # remove *pass* and add 404 code here
            print("HTTP/1.1 400 Not Found\n")


        modify_date = os.path.getmtime(filename)
        print(modify_date)

        # Check if asset is avaialble and the method is correct, serve the asset

        # response += "Date:" + today + "\n"
        # response += "Server: HTTP Server\n"

    return response

def main(argv):
    port = int(argv[0]) # arbitrary non-privileged port
    host = ''  # symbolic name meaning all available interfaces

    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the server to the port
    s.bind((host, port))
    s.listen(1)
    print('Listening for connections on port:', port)
    while 1:
        conn, addr = s.accept()
        # message = conn.recv(1024).decode('UTF-8','replace').strip()
        message = conn.recv(1024)

        # decode the message and respond
        # response = handle_request(message) #Alternate Way 
        response = handle_request(message.decode('UTF-8'))
        conn.send(response)
        # conn.send(bytes(response, 'UTF-8'))
        conn.close()

    # signal our intent to close the socket and then close it
    # the shutdown step is _essentially_ optional
    s.shutdown(socket.SHUT_RDWR)
    s.close()


if __name__ == "__main__":
    # pass arguments if any exist, otherwise send some defaults (not complete)
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main([9000])
