# find_dust_spot.py
import math

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

   def setMap(self): # a
      Map[0][0] = self.a1
      Map[0][MAX_SIZE-1] = self.a2
      Map[MAX_SIZE-1][0] = self.a3
      Map[MAX_SIZE-1][MAX_SIZE-1] = self.a4
      for i in range(298):
         for j in range(298):
            Map[i+1][j+1] = self.CalPointDust(i+1,j+1)
         #print(Map[i+1])

      
   def getMaxPos(self): 
      max = 0
      pos = [0,0]
      for i in range(298):
         for j in range(298):
            if Map[i+1][j+1] >max:
               max = Map[i+1][j+1]
               pos[0] = i+1
               pos[1] = j+1
      return pos
      

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

   def setMiniMap(self):
      for i in range(0,30):
         for j in range(0,30):
            miniMap[i][j] = self.CalAverageValue(i,j)
      miniMap[0][0] = Map[0][0]
      miniMap[0][29] = Map[0][299]
      miniMap[29][0] = Map[299][0]
      miniMap[29][29] = Map[299][299]
   
   def printMap(self):
      print(Map)
   
   def printMiniMap(self):
      for i in range(30):
         print(miniMap[i])
      
   
   def CalAverageValue(self,x,y):
      cnt=0
      sum = 0
      for i in range(x*10,(x+1)*10):
         for j in range(y*10,(y+1)*10):
            if Map[i][j] !=0:
               cnt = cnt+1
            sum = sum + Map[i][j]

      return sum/cnt
         
