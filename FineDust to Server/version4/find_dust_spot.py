# find_dust_spot.py
import math
from websocket import create_connection
import time

MAX_SIZE = 300
Map =[[0]*300 for i in range(300)] # 모든원소가 0인 300x300 리스트
miniMap =[[0]*30 for i in range(30)] # 모든원소가 0인 30x30 리스트

class FindDust: 
   def __init__(self, a1,a2,a3,a4):
      self.a1 = a1
      self.a2 = a2
      self.a3 = a3
      self.a4 = a4

   def getA1(self):
      return self.a1
   def getA2(self):
      return self.a2
   def getA3(self):
      return self.a3
   def getA4(self):
      return self.a4

   def setA1(self,a1):
      self.a1 = a1
   def setA2(self,a2):
      self.a2 = a2
   def setA3(self,a3):
      self.a3= a3
   def setA4(self,a4):
      self.a4 = a4

   def setDust(self, a1,a2,a3,a4):
      self.a1 = a1
      self.a2 = a2
      self.a3 = a3
      self.a4 = a4
   

   def CalPointDust(self, x,y):
      d1=self.distance(x,y,0,0)
      d2=self.distance(x,y,0,MAX_SIZE-1)
      d3=self.distance(x,y,MAX_SIZE-1,0)
      d4=self.distance(x,y,MAX_SIZE-1,MAX_SIZE-1)

      r1 = self.a1-(d1*self.a1/(300*math.sqrt(2)))
      r2 = self.a2-(d2*self.a2/(300*math.sqrt(2)))
      r3 = self.a3-(d3*self.a3/(300*math.sqrt(2)))
      r4 = self.a4-(d4*self.a4/(300*math.sqrt(2)))
      
      return r1 + r2 + r3 + r4
      
   def distance(self,src_x,src_y,dest_x,dest_y):
      return math.sqrt(math.pow((dest_x-src_x),2) + math.pow((dest_y-src_y),2))
   
   
   def CalAverageValue(self,x,y):
      cnt=0
      sum = 0
      for i in range(x*10,(x+1)*10):
         for j in range(y*10,(y+1)*10):
            if Map[i][j] !=0:
               cnt = cnt+1
            sum = sum + Map[i][j]

      return sum/cnt

   def printFile(self):
      file = open("text.txt","w")
      for i in range(0,30):
         file.write(', '.join(miniMap[i]))
         file.write("\n")

      file.close()

   def getMessage(self):
      result =""
      result = result + str(self.getA1()) +","+str(self.getA2())+","+ str(self.getA3())+","+ str(self.getA4()) 
      return result

   def sendMap(self):
      ws = create_connection("ws://15.164.166.134:8000/")
      while(True) :
         print("Sending 'Hello, World'...")
         ws.send(self.getMessage())
         print("Sent")
         print("Receiving...")
         result =  ws.recv()
         print("Received '%s'" % result)
         time.sleep(2)
      ws.close()

   def getMoveDistance(self, src_x,src_y, dest_x,dest_y):
        return self.distance(src_x,src_y,dest_x,dest_y)*79/300

   def getMoveRad(self, src_x,src_y, dest_x,dest_y,src_rad):
      return math.atan2((dest_y-src_y),(dest_x-src_x))-src_rad*0.00001

   def getDest(self, a1,a2,a3,a4):
      arr = [a1,a2,a3,a4]
      max_value = max(arr)

      if max_value >50:
         return (arr.index(max(arr)) +1)
      else:
         return 0

   