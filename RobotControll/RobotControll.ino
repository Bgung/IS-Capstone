#include "RobotController.hpp"

RobotController robotController = RobotController();

const byte BTN = 10;
int STATE = 1;
void setup()
{
  pinMode(BTN, INPUT);
  setupSerial();
}
 
void loop()
{
  int D = digitalRead(BTN);
  if(D == HIGH){
    if(STATE == 0) {
      STATE = 1;
    } else {
      STATE = 0;
    }
  }
  if(STATE == 0){
    robotController.stop();
  } else {
    readOperation(robotController);
  }
}
void setupSerial(){
  Serial.begin(115200);
}

void readOperation(RobotController robotController){
  int readLen = Serial.available();
  if(readLen){
    for(int i = 0; i < readLen; i++){
      char operation = Serial.read();
      int power = Serial.parseInt();
      Serial.println(operation);
      Serial.println(power);
      switch(operation){
        case 'F':
        case 'f':
          robotController.forward(power);
          break;
        case 'B':
        case 'b':
          robotController.backward(power);
          break;
        case 'R':
        case 'r':
          robotController.right(power);
          break;
        case 'L':
        case 'l':
          robotController.left(power);
          break;
        case 'S':
        case 's':
          robotController.stop();
          break;
      }
    }
  }
}