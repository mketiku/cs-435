#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# import os
import socket
import sys

'''Application acts as client for a smtp message.'''
__author__ = "Michael Ketiku"
__project__ = "minismtpclient"
___email__ = "mketiku@gmail.com"
___date__ = "10-03-16"
___status__ = "stable"


# define the port and host we want to connect to
PORT = 25
HOST = 'bumail.butler.edu'

greeting = 'EHLO ' + HOST + '\r\n'
sender = 'MAIL FROM: mketiku@butler.edu\r\n'
receiver = 'RCPT TO: mketiku@butler.edu\r\n'
data = 'DATA\r\n'
text = 'Subject: Checking In\r\nHey Michael, How is it going?\r\n.\r\n '
quit = 'QUIT\r\n'


def main(argv):
    # create an INET, STREAMing socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # connect the client to given host and port
        s.connect((HOST, PORT))

        # s.create_connection(host, port)
        message = [
            greeting, sender, receiver, data, text, quit]
        for item in message:
            respon = s.recv(4096)
            print(str(respon, 'utf-8').upper())
            print(item)
            s.sendall(item.encode('utf-8'))

        s.shutdown(socket.SHUT_RDWR)
        s.close()
    # signal our intent to close the socket and then close it
    # the shutdown step is _essentially_ optional

if __name__ == "__main__":
    # pass arguments if any exist, otherwise send some defaults (not complete)
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        main([PORT])
