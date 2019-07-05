# find_dust_spot.py
import math

MAX_SIZE = 300
Map =[[0]*300 for i in range(300)] # 모든원소가 0인 300x300 리스트
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

   def getDest(self):
      Map[0][0] = self.a1
      Map[0][MAX_SIZE-1] = self.a2
      Map[MAX_SIZE-1][0] = self.a3
      Map[MAX_SIZE-1][MAX_SIZE-1] = self.a4
      for i in range(298):
         for j in range(298):
            Map[i+1][j+1] = self.CalPointDust(i+1,j+1)
         #print(Map[i+1])

      

      max_pos = self.MaxPos()
      return max_pos

   def MaxPos(self): 
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

      r1 = self.a1-(d1*self.a1/300*math.sqrt(2))
      r2 = self.a2-(d2*self.a2/300*math.sqrt(2))
      r3 = self.a3-(d3*self.a3/300*math.sqrt(2))
      r4 = self.a4-(d4*self.a4/300*math.sqrt(2))
      

      return r1 + r2 + r3 + r4
      
   def distance(self,src_x,src_y,dest_x,dest_y):
      return math.sqrt(math.pow((dest_x-src_x),2) + math.pow((dest_y-src_y),2))
      
