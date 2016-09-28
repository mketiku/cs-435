#!/usr/bin/env python3

import datetime
import os
import socket
import sys

# datetime format
format = "%a, %d %b %Y %H:%M:%S %Z"

# we'll store html and other files in an html directory
wwwroot = "{}/html/".format(os.getcwd())
requested_file = "/index.html"

# dictionaries to look up valid content-types and response code messages
# referencing codes['200'] will return 'OK'
content_types = { 'html': 'text/html', 'css': 'text/css', 'js': 'application/x-javascript', 'jpg': 'image/jpeg', 'gif': 'image/gif', 'png': 'image/png'}
codes = { '200': 'OK', '304': 'Not Modified', '404': 'Not Found', '405': 'Method Not Allowed'}

def handle_request(request):
    '''Disassemble the request and create a response message.'''
    req = request.split("\n")[0] # create a list of items from the first line of the message
    headers = parse_headers(request) # create a dictionary of header/value pairs
    request_headers = req

    # use the items() method to iterate over keys and values in a dictionary
    for h,v in headers.items():
        print("{} => {}".format(h,v))

    # check HTTP method is allowed and, if not, create response

    # check for if-modified-since and respond if not modified

    # to read the datetime string in a request we can specify the formatting and create a datetime object
    # datetime.datetime.strptime(v, format)

    # request_method = req.split(' ')[0]
    # assert(request_method == 'GET')
    #
    # if (requested_file == '/'):
    #     requested_file = '/index.html'

    print(request_headers)

    # to get a datetime object for *right now*
    # today = datetime.datetime.today()

    # finally
    try:
        filename = "{}{}".format(wwwroot, requested_file)

        # determine content-type (can also be done inline when creating a response message)

	# the pythonic way to open files ... will close files automatically
        with open(filename) as f:
            # read the file and append it to the response message
            # use 'f.read()' to read the file contents
            response = request_headers + f.read()

    except IOError:
        # 404 response ... file not found
	# remove *pass* and add 404 code here
        pass
    except:
        print('HTTP/1.1 404 Not Found\n')

    return response


def parse_headers(request):
    '''Return a dictionary in the form Header => Value for all headers in *request*.'''
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

    #create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # now bind the server to the port
    s.bind(('', port))
    s.listen(1)
    print('Listening for connections on Port', port)
    while 1:
        conn, addr = s.accept()
        message = conn.recv(1024)

	# decode the message and respond
        response = handle_request(message.decode('UTF-8'))
        conn.send(bytes(response,'UTF-8'))
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
        main( [43500] )