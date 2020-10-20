#!/usr/bin/python3
#-*- coding: utf-8; mode: python -*-

import socket
from struct import *
import base64
import struct

def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
    sum_as_16b_words  = sum16(data)
    sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
    _1s_complement    = ~sum_1s_complement & 0xffff
    return _1s_complement

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost',3459))

while True:
    task , client = sock.recvfrom(1024)
    print("packed info")
    print(task)
    print(task[8:len(task)])


    unpacked_info = unpack('3sBHH'+ str(len(task[8:len(task)])) +'s',task)
    print("unpacked info")
    print(unpacked_info)

    print(unpacked_info[0].decode())
    print(unpacked_info[1])
    print(unpacked_info[2])
    print(str(cksum(task[8:len(task)])))
    print(unpacked_info[3])
    print(str(base64.b64decode(unpacked_info[4]).decode()))


    #sock.sendto("adios".encode(),client)