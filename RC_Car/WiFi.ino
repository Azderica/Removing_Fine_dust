#include <SoftwareSerial.h>
#define LEFT1 5
#define LEFT2 6
#define RIGHT1 10
#define RIGHT2 11

const byte txPin = 2; // Wire this to Tx Pin of ESP8266
const byte rxPin = 3; // Wire this to Rx Pin of ESP8266

String AP = "DONGWOOK";       // CHANGE ME
String PASS = "tbfbr1211"; // CHANGE ME

String HOST = "192.168.43.160";//Host IP or Address
String PORT = "9009";//Port num
String Reply = "OK";
String inData;

/*Car Wheel variables*/
int straight = 0;
int lturn = 0;
int rturn = 0;
float speed_adjust = 1;
int speed_ml = 170*speed_adjust;
int speed_mr = 145*speed_adjust;
int stop_m = 0;

SoftwareSerial ESP8266 (rxPin, txPin);//Software Serial for ESP8266

void WaitForMessage(){
  delay(2000);
   while (ESP8266.available())
   {
     inData = ESP8266.readStringUntil('\n');
     Serial.println("Got reponse from ESP8266: " + inData);
   }
}

void WaitForConnection(){
  delay(2000);
   while (inData.indexOf("OK")==-1)
   {
     inData = ESP8266.readStringUntil('\n');
   }
   Serial.println("WiFi Connected!");
   delay(2000);
}

void WaitForLink(){
  delay(2000);
   while (inData.indexOf("Linked")==-1)
   {
     inData = ESP8266.readStringUntil('\n');
     Serial.println(inData);
   }
   Serial.println("Server Connected!");
}

void Movedata()
{
  int meslen = 0;
  int rad = 0;
  int distance = 0;
  char mesary[100]={0};
  char buffer[100]={0};
   while (ESP8266.available()){
     String Movedata = ESP8266.readStringUntil('\n');
     if((Movedata.indexOf("IPD"))<0)
     {
      /*Command, 
      Blanck messages are filtered here.*/
       continue;
     }
     Serial.println("Original message from ESP8266: " + Movedata);
     Movedata.toCharArray(mesary,Movedata.length());
     sscanf(mesary,"+IPD,%d:%d,%d\n",&meslen,&rad,&distance);
     sprintf(buffer,"rad = %d, distance = %d\n",rad,distance);
     Serial.print(buffer);
     MoveCar(rad,distance);
  }  
}

void MoveCar(int rad, int dist)
{
  if(rad) //have to rotate
  {
    if(rad<0)//counter-clockwise rotation
    {
      Serial.println("rotating counter-clockwise. . .");
      analogWrite(LEFT1,stop_m);
      analogWrite(LEFT2,speed_ml);
      analogWrite(RIGHT1,speed_mr);
      analogWrite(RIGHT2,stop_m);
      delay(abs(rad));
      analogWrite(LEFT1,stop_m);
      analogWrite(LEFT2,stop_m);
      analogWrite(RIGHT1,stop_m);
      analogWrite(RIGHT2,stop_m);
    }
    else//clockwise rotation
    {
      Serial.println("rotating clockwise. . .");
      analogWrite(LEFT1,speed_ml);
      analogWrite(LEFT2,stop_m);
      analogWrite(RIGHT1,stop_m);
      analogWrite(RIGHT2,speed_mr);;
      delay(rad);
      analogWrite(LEFT1,stop_m);
      analogWrite(LEFT2,stop_m);
      analogWrite(RIGHT1,stop_m);
      analogWrite(RIGHT2,stop_m);
    }
  }
  if(dist)//have to move
  {
    Serial.println("moving straight..\n");
    analogWrite(LEFT1,stop_m);
    analogWrite(LEFT2,speed_ml);
    analogWrite(RIGHT1,stop_m);
    analogWrite(RIGHT2,speed_mr);
    delay(dist);
    analogWrite(LEFT1,stop_m);
    analogWrite(LEFT2,stop_m);
    analogWrite(RIGHT1,stop_m);
    analogWrite(RIGHT2,stop_m);
  }
}
void setup() {
  Serial.begin(9600);
  /*Pin setting for wheels of car*/
  pinMode(LEFT1,OUTPUT);
  pinMode(LEFT2,OUTPUT);
  pinMode(RIGHT1,OUTPUT);
  pinMode(RIGHT2,OUTPUT);
  
  ESP8266.begin(9600); // Change this to the baudrate used by ESP8266
  Serial.println("Checking Connection of ESP8266 . . .");
  ESP8266.println("AT");
  WaitForMessage();
  Serial.println("Initializing Connection. . .");
   ESP8266.println("AT+CWMODE=1");
  WaitForMessage();
//  ESP8266.println("AT+CIFSR");
//  Serial.println("AT+CIFSR");
//  WaitForMessage();
   ESP8266.println("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"");
  Serial.println("AT+CWJAP=\""+ AP +"\",\""+ PASS +"\"");
  WaitForConnection();
  ESP8266.println("AT+CIPSTART=\"TCP\",\""+ HOST +"\","+ PORT);
  Serial.println("AT+CIPSTART=\"TCP\",\""+ HOST +"\","+ PORT);
  WaitForLink();
}
void loop() {
  Movedata();
}
