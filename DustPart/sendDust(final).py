#multi_threaded client

import socket
from threading import Thread
import time
import serial

HOST = '192.168.43.41'
APORT = '/dev/ttyACM0'
APORT2 = '/dev/ttyACM1'
APORT3 = '/dev/ttyACM2'
APORT4 = '/dev/ttyACM3'
PORT = 9009
BaoudRate = 9600

s = serial.Serial(APORT,BaoudRate)
s2 = serial.Serial(APORT2,BaoudRate)
s3 = serial.Serial(APORT3,BaoudRate)
s4 = serial.Serial(APORT3,BaoudRate)

def rcvMsg(sock):
   while True:
      try:
         data = sock.recv(1024)
         if not data:
            break
         print(data.decode())
      except:
         pass

def sendDust():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       sock.connect((HOST, PORT))
       t = Thread(target=rcvMsg, args=(sock,))
       t.daemon = True
       t.start()
       msg = 'DustInfo'
       msg = bytes(msg,'utf-8')
       sock.send(msg)

    while True:

        if(s.readable()):
            dust = s.readline()
            dust2 = s2.readline()
            dust3 = s3.readline()
            dust4 = s4.readline()

            data = dust + ',' + dust2 + ',' + dust3 + ',' + dust4 + ','
            data = bytes(data,'utf-8')
            sock.send(data);

            time.sleep(5)

        else:
            print("read impossible")

sendDust()
