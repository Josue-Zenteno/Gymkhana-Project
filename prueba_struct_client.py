#!/usr/bin/python3
#-*- coding: utf-8; mode: python -*-

import socket
import base64
import struct
from struct import *

def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
    sum_as_16b_words  = sum16(data)
    sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
    _1s_complement    = ~sum_1s_complement & 0xffff
    return _1s_complement

r_WYP = "WYP".encode()
r_type = 0
r_code = 0
r_cksum = 0
r_payload = base64.b64encode("8a012cf4-8686-11ea-9191-0800278dc04d".encode())

print('base64: '+ str(r_payload)+'\n')
print('normal: '+ str(base64.b64decode(r_payload))+'\n')

packed_info = pack('3sBHH'+str(len(r_payload))+'s',r_WYP,r_type,r_code,r_cksum,r_payload)
print("packed_info")
print(packed_info)
print("")


r_cksum = cksum(packed_info)

def_packed_info = pack('3sBHH'+str(len(r_payload))+'s',r_WYP,r_type,r_code,r_cksum,r_payload)

print("packed_info")
print(packed_info)
print("")

unpakced_info = unpack('3sBHH'+ str(len(r_payload)) +'s',packed_info)
print("unpacked info")
print(unpakced_info)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.sendto(packed_info,('localhost',3459))






def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
    sum_as_16b_words  = sum16(data)
    sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
    _1s_complement    = ~sum_1s_complement & 0xffff
    return _1s_complement



