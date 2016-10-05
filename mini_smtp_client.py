#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import socket
import sys

'''Application acts as client for a smtp message.'''
__author__ = "Michael Ketiku"
__project__ = "minismtpclient"
___email__ = "mketiku@gmail.com"
___status__ = "final"

def main(argv):
    port = argv[0]

    #create an INET, STREAMing socket
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    # now bind the server to the port
    s.bind(('', port))
    s.listen(1)
    print('Listening for messages')
    while 1:
        conn, addr = s.accept()
        message = conn.recv(1024)
        response = message.decode('UTF-8').upper()
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
        main( [43500] )
