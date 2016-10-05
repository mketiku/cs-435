#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import datetime
import os
import socket
import sys

'''Application serves a simple web directory.'''
__author__ = "Michael Ketiku"
__project__ = "SimpleHttpServer"
___email__ = "mketiku@gmail.com"
___status__ = "final"

# datetime format
obj_time_format = "%a, %d %b %Y %H:%M:%S %Z"
req_time_format = '%Y-%m-%d %H:%M:%S.%f'

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
    'png': 'image/png',
    'ico': 'image/ico'
}

# response_header = 'hello moto'
# response = ''


def parse_headers(request):
    """Return a dictionary in the form Header
    => Value for all headers in *request*.

    """
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
    req = request.split(
        "\n")[0]  # create a list of items from the first line of the message
    # create a dictionary of header/value pairs
    headers = parse_headers(request)

    print('>  Request:  {}'.format(req))
    # check HTTP method is allowed and, if not, create response
    if req != '':
        method = req.split(' ')[0]
        print(">  Method:", method)
        requested_file = req.split(' ')[1]
    else:
        method = 'GET'
        print(">  Method:", method)
        requested_file = "/"

    if requested_file.endswith("/"):
        print(">  Method:", method)
        requested_file = requested_file + "index.html"

    print('>  Object: ' + requested_file.replace("/", ""))

    # use the items() method to iterate over keys and values in a dictionary
    for h, v in headers.items():
        print("{} => {}".format(h, v))

    # check for if-modified-since and respond if not modified

    # to read the datetime string in a request we can specify the formatting
    # and create a datetime object
    # datetime.datetime.strptime(v, format)
    # # response_header = today +
    #
    # # to get a datetime object for *right now*
    today = datetime.datetime.today()
    #
    # response_header = today
    # print(today)
    if method in permitted_methods:
            # determine the content type
        print(">  Method:", method, "Allowed")
        content_type = os.path.splitext(requested_file)[1].replace(".", "")
        if content_type in permitted_types:
            print(">  Content Type:", permitted_types[content_type], "Allowed")
            try:
                # requested_file = "index.html"
                filename = "{}{}".format(wwwroot, requested_file)

                # the pythonic way to open files ... will close files
                # automatically
                with open(filename, mode='rb') as f:
                    # read the file and append it to the response message
                    # use 'f.read()' to read the file contents
                    if os.path.isfile(filename):
                        print(">  Response: HTTP/1.1 200 OK\n")
                    response = f.read()
                    # response = bytes(response_header, 'UTF-8') + f.read()

                    modify_date = datetime.datetime.fromtimestamp(
                        os.path.getmtime(filename))
                    print(">  Last Modified:", modify_date)
                    if 'if-modified-since' in h:
                        check_date = datetime.datetime.strptime(
                            h['if-modified-since'], req_time_format)
                        elapsed_time = check_date - modify_date
                        if elapsed_time > datetime.timedelta(seconds=0):
                            print(">  Code: 304 Not Modified")

            except (IOError, OSError) as e:
                # 404 response ... file not found
                # remove *pass* and add 404 code here
                print(">  Response: HTTP/1.1 400 Not Found\n")
                # response = '/404.html'

        else:
            print(">  Content Type:", permitted_types[
                  content_type], "Not Allowed")
    else:
        print(">  Method:", method, "Not Allowed")

    return response


def main(argv):
    port = int(argv[0])  # arbitrary non-privileged port
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
