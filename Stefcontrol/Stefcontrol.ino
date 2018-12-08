#include <Servo.h>
Servo myservo;
Servo moservo; 
String inByte;
String onByte;
String dir;
String ver;
int pos = 90;
int pis = 25;

void setup() {
 
  myservo.attach(9);
  moservo.attach(10);
  myservo.write(pos);    //initialize servos
  moservo.write(pis);
  Serial.begin(115200);
}

void loop()
{    
  if(Serial.available())  // if data available in serial port
    { 
    inByte = Serial.readStringUntil(','); // read data until newline
    onByte = Serial.readStringUntil('\n');
    dir = inByte;   // change datatype from string to integer 
    ver = onByte; 
    if(dir == "left"){
      pos += 5;
    }
    if(dir == "right"){
      pos -= 5;
    }
    if(ver == "up"){
      pis -= 5;
    }
    if(ver == "down"){
      pis += 5;
    }
    myservo.write(pos);     // move servo
    moservo.write(pis);
    //Serial.print("Servo1 in position: ");  
    //Serial.println(pos);
    //Serial.print("Servo2 in position: ");  
    //Serial.println(pis);
    }
}
