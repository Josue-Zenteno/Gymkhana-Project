#!/usr/bin/python3
#-*- coding: utf-8; mode: python -*-

#Libraries

import socket
import hashlib
import base64
import struct
from struct import *

#Author : JOSUE CARLOS ZENTENO YAVE
#Year : 2020 
#Auxiliar functions
"""
"Internet checksum algorithm RFC-1071"
Copyright (C) 2009-2020  David Villa Alises
"""
def sum16(data):
    if len(data) % 2:
        data = b'\0' + data

    return sum(struct.unpack('!%sH' % (len(data) // 2), data))


def cksum(data):
    sum_as_16b_words  = sum16(data)
    sum_1s_complement = sum16(struct.pack('!L', sum_as_16b_words))
    _1s_complement    = ~sum_1s_complement & 0xffff
    return _1s_complement

#Principal program

def main():
    code0 = reto_0()
    code1 = reto_1(code0)
    code2 = reto_2(code1)
    code3 = reto_3(code2)
    code4 = reto_4(code3)
    reto_5(code4)

def reto_0 ():

    #Socket creation and connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('node1',2000))

    #Recieving the Data
    print(sock.recv(1024).decode())

    #Dealing with the task
    sock.send('josuecarlos.zenteno'.encode())

    #Printing the next task
    task = (sock.recv(1024).decode())
    print(task)

    #Free resources
    sock.close()

    #Return the code for the next task
    return task[:36]
    
def reto_1 (identifier0):
    
    #Socket creation and binding
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',3459))

    #Dealing with the task
    sock.sendto(("3459 "+identifier0).encode(),('node1',3000))

    #Printing the next task
    task , client = sock.recvfrom(1024)
    print(task.decode())

    #Free resources
    sock.close()

    #Return the code for the next task
    return task.decode()[5:41]

def reto_2(identifier):

    #Socket creation and connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('node1',4001))

    #Dealing with the task
    data = b'' 
    sero = False #When 0 is found the task is terminated

    while (sero == False):
        data += sock.recv(1024) 
        counter = 0
        i=0
        numbers_vector = data.decode().split(sep = None, maxsplit= -1) #This works as an String Tokenizer

        while ((i<len(numbers_vector)) and (sero == False)):
            if(numbers_vector[i] == '0'):
                sero = True
            else:
                counter += 1
                i += 1

    sock.send((identifier +" "+ str(counter)).encode())

    #Printing the next task
    task = b''
    while(True):
        aux = sock.recv(1024)
        if len(aux) <= 0:
            break
        task += aux
    
    print(task.decode())
    
    #Free resources
    sock.close()

    #Return the code for the next task
    code_from_task = task.decode().split(sep = ':',maxsplit = 2)
    return code_from_task[1][0:36]
    
def reto_3(identifier):

    #Socket creation and connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('node1',6000))

    #Dealing with the task
    data = b''
    palindrome = False

    while (palindrome == False):
        data += sock.recv(1024)
        words_vector = data.decode().split(sep=' ',maxsplit=-1)
        final_string = ""
        i=0
        while((i<len(words_vector))and(palindrome == False)):
            
            if(words_vector[i].isnumeric()):
                if (len(final_string) != 0):
                    final_string += " "
                final_string += words_vector[i]
            else:
                if((words_vector[i] == words_vector[i][::-1]) and (len(words_vector[i]) != 1)):
                    palindrome = True
                else:
                    if (len(final_string) != 0):
                        final_string += " "
                    final_string += words_vector[i][::-1]
            i += 1

    sock.send(final_string.encode())
    sock.send(("--"+identifier+"--").encode())

    #Printing the next task

    task = b''
    while(True):
        aux = sock.recv(1024)
        if len(aux) <= 0:
            break
        task += aux

    print(task.decode())

    #Free resources
    sock.close()

    #Return the code for the next task
    code_from_task = task.decode().split(sep = ':',maxsplit = 2)
    return code_from_task[1][0:36]

def reto_4(identifier):

    #Socket creation and connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('node1',10000))
    
    #Dealing with the task

    hashifier = hashlib.md5()

    sock.send(identifier.encode())

    dots_found = False
    s_file_size = ""

    while (dots_found == False):
        aux = sock.recv(1)
        if (aux.decode() == ':'):
            dots_found = True
        else:
            s_file_size += aux.decode()

   
    file = b''
    i_file_size = int(s_file_size)

    while (i_file_size > len(file)):
        file += sock.recv(1024)
        
    
    hashifier.update(file)
    sock.send(hashifier.digest())

    #Printing the next task
    
    task = b''
    while(True):
        aux = sock.recv(1024)
        if len(aux) <= 0:
            break
        task += aux
    
    print(task.decode())
        
    
    #Free resources
    sock.close()
    
    #Return the code for the next task
    return task.decode()[5:41]


def reto_5 (identifier):

    #socket creation
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #Dealing with the task
    r_WYP = b'WYP'
    r_type = 0
    r_code = 0
    r_cksum = 0
    r_payload = base64.b64encode(str(identifier).encode())
    
    packed_info = pack('3sBHH',r_WYP,r_type,r_code,r_cksum)
    
    r_cksum = cksum(packed_info+r_payload)
    
    def_packed_info = pack('!3sBHH'+str(len(r_payload))+'s',r_WYP,r_type,r_code,r_cksum,r_payload)

    sock.sendto(def_packed_info,('node1',7001))

    #printing the next task
    task , esi_server = sock.recvfrom(2048)
    unpacked_info = unpack('!3sBHH'+ str(len(task[8:len(task)])) +'s',task)
    print(base64.b64decode(unpacked_info[4]).decode())

    #Free resources
    sock.close()



try:
    main()
except KeyboardInterrupt:
    pass 

