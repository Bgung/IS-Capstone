#define DEFAULT_POWER 85

//회전 방향
#define CW 1 //clockwise rotation
#define CCW 0 //counter-clockwise

#define MOTOR_LEFT 0
#define MOTOR_RIGHT 1

// 아두이노 PIN 설정
const byte PWMA = 3;      // PWM control (speed) for motor A
const byte PWMB = 11;     // PWM control (speed) for motor B
const byte DIRA = 12;     // Direction control for motor A
const byte DIRB = 13;     // Direction control for motor B

void setup()
{
  // initialization
  setupArdumoto();
  setupSerial();

  Serial.println(OUTPUT);
  Serial.println(HIGH);
  Serial.println(LOW);
}
 
void loop()
{
  readOperation();
}
void setupSerial(){
  Serial.begin(115200);
}

void readOperation(){
  int readLen = Serial.available();
  if(readLen){
    for(int i = 0; i < readLen; i++){
      char operation = Serial.read();
      int power = Serial.parseInt();
      Serial.println(operation);
      Serial.println(power);
      executeOperation(operation, power);
    }
  }
}
void executeOperation(char direction, int power){
    if (power > 0 && power < 255){
      power = power;
    } else {
      power = DEFAULT_POWER;
    }
    switch(direction){
      case 'F':
        robotForward(power);
        break;
      case 'B':
        robotBackward(power);
        break;
      case 'L':
        robotLeft(power);
        break;
      case 'R':
        robotRight(power);
        break;
      case 'S':
        robotStop();
        break;
      default:
        break;
    }  
}
  // setupArdumoto initialize all pins
void setupArdumoto()
{
  // All pins should be setup as outputs:
  pinMode(PWMA, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DIRA, OUTPUT);
  pinMode(DIRB, OUTPUT);
  
  // Initialize all pins as low:
  digitalWrite(PWMA, LOW);
  digitalWrite(PWMB, LOW);
  digitalWrite(DIRA, LOW);
  digitalWrite(DIRB, LOW);
}



void driveArdumoto(byte motor, byte dir, byte spd)
{
  if(motor == MOTOR_LEFT)
  {
    digitalWrite(DIRA, dir);
    analogWrite(PWMA, spd);
  }
  else if(motor == MOTOR_RIGHT)
  {
    digitalWrite(DIRB, dir);
    analogWrite(PWMB, spd);
  }  
}

void robotForward(unsigned char velocity)
{
  driveArdumoto(MOTOR_LEFT, CW, velocity);
  driveArdumoto(MOTOR_RIGHT, CCW, velocity);
}

void robotBackward(unsigned char velocity)
{
  driveArdumoto(MOTOR_LEFT, CCW, velocity);
  driveArdumoto(MOTOR_RIGHT, CW, velocity);
}

void robotRight(unsigned char velocity)
{
  driveArdumoto(MOTOR_LEFT, CCW, velocity);
  driveArdumoto(MOTOR_RIGHT, CCW, velocity);
}

void robotLeft(unsigned char velocity)
{
  driveArdumoto(MOTOR_LEFT, CW, velocity);
  driveArdumoto(MOTOR_RIGHT, CW, velocity);
}

// stopArdumoto makes a motor stop
void stopArdumoto(byte motor)
{
  driveArdumoto(motor, 0, 0);
}

void robotStop()
{
  stopArdumoto(MOTOR_LEFT);
  stopArdumoto(MOTOR_RIGHT);
}