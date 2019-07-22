#multi_threaded client

import socket
from threading import Thread
import time
import serial

HOST = '192.168.43.160'
APORT = '/dev/ttyACM0'
PORT = 9009
BaoudRate = 9600

s = serial.Serial(APORT,BaoudRate)

def rcvMsg(sock):
   while True:
      try:
         data = sock.recv(1024)
         if not data:
            break
         print(data.decode())
      except:
         pass
 
def runChat():
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((HOST, PORT))
      t = Thread(target=rcvMsg, args=(sock,))
      t.daemon = True
      t.start()
      num = 0
      msg = input()
      sock.send(msg.encode())
      cnt=0
      
      while True:
        if(s.readable()):
            num = s.readline()
            print(num)
            count = str(cnt)+":"+str(num)
            count = bytes(count,'utf-8')
            sock.send(count)
            cnt = cnt+1
            time.sleep(5)        
        else:
            print("read impossible")
             
runChat()
