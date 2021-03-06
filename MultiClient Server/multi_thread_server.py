# multi_threaded server

import socketserver
import socket
import threading
import time
import find_dust_spot
from websocket import create_connection
import random

from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json

HOST = ''
PORT = 9009
url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst'
queryParams = '?serviceKey=Dc6ewA1eR8iB5JzsB5vrC8Bt9Xs%2F43rSAnXksoR3ZYoaAs3qb%2F8sfb8zeMdDtg4ZHrnEO4j1aSQCQshB5h2P1A%3D%3D&numOfRows=10&pageNo=1&sidoName=%EB%8C%80%EA%B5%AC&searchCondition=DAILY&_returnType=json'
dict = ""

class Arduino: #아두이노 미세먼지 모듈
   def __init__(self,msg):
      temp = msg.split("\\r\\n',")
      self.a1 = int(temp[0][2:])
      #print(self.a1)
      self.a2 = int(temp[1][2:])
      #print(self.a2)
      self.a3 = int(temp[2][2:])
      #print(self.a3)
      self.a4 = int(temp[3][2:])
      #print(self.a4)

   def setArduino(self,msg):
      temp = msg.split("\\r\\n',")
      self.a1 = int(temp[0][2:])
      print(self.a1)
      temp = temp[1]
      temp = temp.split(",")
      self.a2 = int(temp[0])
      #self.a2 = random.randint(17,23)
      print(self.a2)
      self.a3 = int(temp[1])
      #self.a3 = random.randint(17,23)
      print(self.a3)
      self.a4 = int(temp[2])
      #self.a4 = random.randint(17,23)
      print(self.a4)

   def getA1(self):
      return self.a1
   def getA2(self):
      return self.a2
   def getA3(self):
      return self.a3
   def getA4(self):
      return self.a4

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

lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성
module ={} #아두이노 저장

module["camera"] = Cleaner("100,100,12345")
module["window"] = 0 #닫힌상태
module["arduino"] = Arduino("b'40\\r\\n',b'20\\r\\n',b'30\\r\\n',b'99\\r\\n',")
dust = find_dust_spot.FindDust(module["arduino"].getA1(),module["arduino"].getA2(),module["arduino"].getA3(),module["arduino"].getA4())
ws = create_connection("ws://15.164.166.134:8000/")
ws.send("1,2,1,2:200,200")
# dust = find_dust_spot.FindDust(0 ,0,0,0)
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
         #print("카메라연결")
         if username in module:
            module[username].setCleaner(msg)
         else:
            module[username]=Cleaner(msg)
         #print(module)
         print(username+" : "+str(module[username].getX())+","+str(module[username].getY())+","+str(module[username].getRad()))
      elif username =="arduino":
         if username in module:
            module[username].setArduino(msg)
         else:
            module[username]=Arduino(msg)
         request = Request(url + queryParams)
         request.get_method = lambda: 'GET'
         response_body = urlopen(request).read()
         dict = json.loads(response_body)
         average = module[username].getA1()+module[username].getA2()+module[username].getA3()+module[username].getA4()
         average = average/4
         print("외부 미세먼지 농도 : "+ dict["list"][4]["pm10Value"])
         print("내부 미세먼지 평균 : "+ str(average))
         dust_msg = str(module["arduino"].getA1())+","+str(module["arduino"].getA2())+","+str(module["arduino"].getA3())+","+str(module["arduino"].getA4())
         dust_msg = dust_msg +":"+str(module["camera"].getX())+","+str(module["camera"].getY()) 
         dust_msg = dust_msg +":"+str(dict["list"][4]["pm10Value"])
         print("sending data to aws : "+ dust_msg)
         ws.send(dust_msg)
         if float(dict["list"][4]["pm10Value"]) < average:#외부농도가 낮을때
            module["window"]=1
         else :
            module["window"]=0
         print(username+" : "+str(module[username].getA1())+","+str(module[username].getA2())+","+str(module[username].getA3())+","+str(module[username].getA4()))
         
      else:
         #print("카메라 말고")
         val = int(msg)
         if username in module:
            module[username].setArduino(val)
         else:
            module[username]=Arduino(msg)
         #print(module)
         #print(username+" : "+str(module[username].getValue()))
         #message = Message(username,msg)
         #print(arduino[username])
         return
 
 
   def sendMessageToAll(self, msg):
      for conn, addr in self.users.values():
         conn.send(msg.encode('utf-8'))
         
   def sendMessageToUser(self, username,msg):
      self.users[username][0].send(msg.encode('utf-8'))
         
class MyTcpHandler(socketserver.BaseRequestHandler):
   userman = UserManager()
     
   def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력
      print('[%s] 연결됨' %self.client_address[0])
      if self.client_address[0]=='192.168.43.194':
         username = 'rccar'
         self.userman.addUser(username, self.request, self.client_address)
         #print("제발")
         while True:
            dest = dust.getDest(module["arduino"].getA1(),module["arduino"].getA2(),module["arduino"].getA3(),module["arduino"].getA4()) 
            
            #dust.sendMap()
           
            #print(module["camera"])
   
            if dest == 1:
               rad = dust.getMoveRad(module["camera"].getX(),module["camera"].getY(),50,350,module["camera"].getRad())
               distance = dust.getMoveDistance(module["camera"].getX(), module["camera"].getY(), 50, 350)
               print("목적지"+str(dest)+":50,350")
            elif dest == 2:
               rad = dust.getMoveRad(module["camera"].getX(),module["camera"].getY(),50,50,module["camera"].getRad())
               distance = dust.getMoveDistance(module["camera"].getX(), module["camera"].getY(), 50, 50)
               print("목적지"+str(dest)+":50,50")
            elif dest == 3:
               rad = dust.getMoveRad(module["camera"].getX(),module["camera"].getY(),350,50,module["camera"].getRad())
               distance = dust.getMoveDistance(module["camera"].getX(), module["camera"].getY(), 350, 50)
               print("목적지"+str(dest)+":400,50")
            elif dest == 4:
               rad = dust.getMoveRad(module["camera"].getX(),module["camera"].getY(),350,350,module["camera"].getRad())
               distance = dust.getMoveDistance(module["camera"].getX(), module["camera"].getY(), 350, 350)
               print("목적지"+str(dest)+":400,350")
            else:
               rad = dust.getMoveRad(module["camera"].getX(),module["camera"].getY(),200,200,module["camera"].getRad())
               distance = dust.getMoveDistance(module["camera"].getX(), module["camera"].getY(), 200, 200)
               print("목적지"+str(dest)+":200,200")
   
            print("getmoverad : "+ str(rad))
            if distance > 10:
               if rad > 0.5:
                  val1 = 150 
                  val2 = 0
               
               elif rad < -0.5:
                  val1 = -150
                  val2 = 0
               else :
                  val1 = 0
                  val2 = 400
            else :
               val1 = 0
               val2 = 0

            if module["window"] == 1:#열려 있을때
               val1 = 0
               val2 = 0
               
            print(str(int(val1))+","+str(val2)+"전송")
            #self.userman.sendMessageToUser(username, str(val1)+",0")
            #self.userman.sendMessageToUser(username, "0,"+str(val2))
            self.userman.sendMessageToUser(username, str(int(val1))+","+str(val2))
            print("전송완료")
            #print("sending data to aws")
            time.sleep(2)
            #dust_msg = dust.getMessage() +":"+"0,0"
            #self.userman.sendMessageToUser(username,"1000,"+str(val2))
            #self.userman.sendMessageToAll("50,50")
         
            
      #if self.client_address[0]=='스텝모터 ip':
         #username = 'window'
         #self.userman.addUser(username, self.request, self.client_address)
         #print("제발")
         #while True:


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

