#include "RobotController.hpp"

RobotController robotController;

#define BTN_PIN 10

void setup()
{
  pinMode(BTN_PIN, INPUT);
  Serial.begin(115200);
  robotController = RobotController();
}
 
void loop()
{
  // int interrupt = digitalRead(BTN_PIN);
  // if(interrupt == HIGH){
  //   robotController.setIsInterrupted(
  //     !robotController.getIsInterrupted()
  //   );
  // }
  if(0){
    robotController.stop();
  } else {
    readOperation(robotController);
  }
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
          robotController.forward(power);
          break;
        case 'B':
          robotController.backward(power);
          break;
        case 'R':
          robotController.right(power);
          break;
        case 'L':
          robotController.left(power);
          break;
        case 'S':
          robotController.stop();
          break;
      }
    }
  }
}