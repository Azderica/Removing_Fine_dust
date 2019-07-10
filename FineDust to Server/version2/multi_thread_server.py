# multi_threaded server

import socketserver
import socket
import threading
import time
from parse import *

HOST = ''
PORT = 9009


lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성
module ={}
#cleaner = None
class UserManager: # 사용자관리 메세지 전송을 담당하는 클래스
   def __init__(self):
      self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}
      message = None

   def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
      if username in self.users: # 이미 등록된 사용자라면
         conn.send('이미 등록된 아두이노입니다.\n'.encode())
         return None
 
      # 새로운 사용자를 등록함
      lock.acquire() # 스레드 동기화를 막기위한 락
      self.users[username] = (conn, addr)
      lock.release() # 업데이트 후 락 해제
 
      #self.sendMessageToAll('아두이노[%s] 연결됨.' %username)
      print('+++ 현재 연결된 아두이노 수: [%d]' %len(self.users))
         
      return username
 
   def removeUser(self, username): #사용자를 제거하는 함수
      if username not in self.users:
         return
 
      lock.acquire()
      del self.users[username]
      lock.release()
 
      #self.sendMessageToAll('아두이노 [%s] 종료' %username)
      print('--- 현재 연결된 아두이노 수 : [%d]' %len(self.users))
 
   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
      
      print('[%s] %s' %(username, msg))

      if username =="camera":
         print("카메라연결")
         if username in module:
            module[username].setCleaner(msg)
         else:
            module[username]=Cleaner(msg)
         print(module)

         print(username+" : "+str(module[username].getX())+","+str(module[username].getY())+","+str(module[username].getRad()))
       
      else:
         print("카메라 말고")
         val = float(msg)*0.01
         if username in module:
            module[username].setArduino(val)
         else:
            module[username]=Arduino(username,msg)
         print(module)
         print(username+" : "+str(module[username].getValue()))
         #message = Message(username,msg)
         #print(arduino[username])
         return
 
 
   def sendMessageToAll(self, msg):
      for conn, addr in self.users.values():
         conn.send(msg.encode('utf-8'))
         
   def sendMessageToUser(self, username,msg):
      self.users[username][0].send(msg.encode('utf-8'))
         
class Arduino: #아두이노 미세먼지 모듈
   def __init__(self,username,msg):
      self.username = username
      self.value = float(msg)*0.01

   def setArduino(self,val):
      self.value = round(self.getValue()*0.3 + val*0.7,2)
      return
   
   def getUsername(self):
      return self.username

   def getValue(self):
      return self.value

class Cleaner: #공기청정기
   def __init__(self,msg):
      temp = msg.split(",")
      self.x =int(temp[0])
      self.y = int(temp[1])
      self.rad = int(temp[2])

   def setCleaner(self,msg):
      temp = msg.split(",")
      self.x =int(temp[0])
      self.y = int(temp[1])
      self.rad = int(temp[2])
      return
   
   def getX(self):
      return self.x
   def getY(self):
      return self.y
   def getRad(self):
      return self.rad
   
class MyTcpHandler(socketserver.BaseRequestHandler):
   userman = UserManager()
     
   def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
      print('[%s] 연결됨' %self.client_address[0])
      if self.client_address[0]=='192.168.43.194':
         username = 'rccar'
         self.userman.addUser(username, self.request, self.client_address)
         #print("제발")
         while True:
            #if self.userman.messageHandler(username, msg.decode()) == -1:
               #self.request.close()
               #break
            print("전송")
            self.userman.sendMessageToUser(username, "0,5000")
            #self.userman.sendMessageToAll("50,50")
            time.sleep(2)
            
               
      else:
         try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
               print(msg.decode())
               if self.userman.messageHandler(username, msg.decode()) == -1:
                  self.request.close()
                  break
               msg = self.request.recv(1024)
                 
         except Exception as e:
            print(e)

      print('[%s] 접속종료' %self.client_address[0])
      self.userman.removeUser(username)
 
   def registerUsername(self):
      while True:
         self.request.send('Enter ID:'.encode())
         username = self.request.recv(1024)
         username = username.decode().strip()
         if self.userman.addUser(username, self.request, self.client_address):
            return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
         
def runServer():
   print('+++ 서버 시작.')
   print('+++ 서버를 끝내려면 Ctrl-C를 누르세요.')
 
   try:
      server = ChatingServer((HOST, PORT), MyTcpHandler)
      server.serve_forever()
   except KeyboardInterrupt:
      print('--- 서버를 종료합니다.')
      server.shutdown()
      server.server_close()

      
def send(sock):
    while True:
        sendData = input('>>>')
        sock.send(sendData.encode('utf-8'))

def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('', recvData.decode('utf-8'))
        



runServer()

