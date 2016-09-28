#!/usr/bin/env python3

import datetime
import os
import socket
import sys

# datetime format
format = "%a, %d %b %Y %H:%M:%S %Z"

# we'll store html and other files in an html directory
wwwroot = "{}/www/".format(os.getcwd())

# dictionaries to look up valid content-types and response code messages
# referencing codes['200'] will return 'OK'
content_types = {'html': 'text/html', 'css': 'text/css', 'js': 'application/x-javascript', 'jpg': 'image/jpeg',
                 'gif': 'image/gif', 'png': 'image/png'}
codes = {'200': 'OK', '304': 'Not Modified', '404': 'Not Found', '405': 'Method Not Allowed'}

response_header = ''
response = ''


def handle_request(request):
    """Disassemble the request and create a response message."""
    req = request.split("\n")[0]  # create a list of items from the first line of the message
    headers = parse_headers(request)  # create a dictionary of header/value pairs
    global response
    # use the items() method to iterate over keys and values in a dictionary
    for h, v in headers.items():
        print("{} => {}".format(h, v))

    # check HTTP method is allowed and, if not, create response

    # check for if-modified-since and respond if not modified

    # to read the datetime string in a request we can specify the formatting and create a datetime object
    # datetime.datetime.strptime(v, format)

    # to get a datetime object for *right now*
    today = datetime.datetime.today()

    # finally
    try:
        # requested_file = req[0]
        requested_file = request[4:]
        filename = "{}{}".format(wwwroot, requested_file)
        print(requested_file)
        # determine content-type (can also be done inline when creating a response message)

        # the pythonic way to open files ... will close files automatically
        with open(filename) as f:
            # read the file and append it to the response message
            # use 'f.read()' to read the file contents
            # response = (response_header + f.read()).join()
             response =  "".join(response_header, f.read())
    except IOError:
        # 404 response ... file not found
        # remove *pass* and add 404 code here
        print("HTTP/1.1 404 Not Found\n")
        pass

    # Check if asset is avaialble and the method is correct, serve the asset
    if os.path.exists(filename):
        print("HTTP/1.1 200 OK\n",requested_file)
    else:
        print("HTTP/1.1 400 Not Found\n",requested_file)

    # response += "Date:" + today + "\n"
    # response += "Server: HTTP Server\n"

    return response


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


def main(argv):
    port = int(argv[0])

    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # now bind the server to the port
    s.bind(('', port))
    s.listen(1)
    print('Listening for connections')
    while 1:
        conn, addr = s.accept()
        message = conn.recv(1024)

        # decode the message and respond
        response = handle_request(message.decode('UTF-8'))

        conn.send(bytes(response, 'UTF-8'))
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
        main([43500])
