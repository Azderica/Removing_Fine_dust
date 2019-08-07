#include <Ethernet.h>
#include <SPI.h>
#include<Stepper.h>

Stepper myStepper(200,3,4,6,7);

int stat=0; // 0:close 1: open


byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};    // mac addr
EthernetClient client;
byte server[] = "192.168.43.160"; //server ip

 
void setup(){
   myStepper.setSpeed(18);
   Serial.begin(9600);
   Ethernet.begin(mac);                      
   delay(1000);

   Serial.println("connecting...");
   client.connect(server, 9009);            
   if (client.connected()) {
     Serial.println("connected");
  }

  else{ 
    Serial.println("fail");
  }
}

 

void loop()
{
  
   int len = client.available();

   if(len > 0)
   {
      char buff[80];

      client.read(buff,len);

      if(buff == '1' && stat == 0) // open
      {
         Serial.println("open");
         stat = 1;
         myStepper.step(2048);
      }
      else if(buff == '1' && stat==1) //open
      {
          Serial.println("open");
      }
      else if(buff == '0' && stat==0) //close
      { 
          Serial.println("close");
      }
      else if(buff == '0' && stat==1) // close
      {
         Serial.println("close");
         stat = 0;
         myStepper.step(-2048); 
    
      }
   }
}
