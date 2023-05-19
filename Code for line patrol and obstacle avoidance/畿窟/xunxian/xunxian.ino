//电机引脚
#define PWMA 12    //A电机转速
#define DIRA1 34 
#define DIRA2 35  //A电机方向
#define PWMB 8    //B电机转速
#define DIRB1 37 
#define DIRB2 36  //B电机方向
#define PWMC 9    //C电机转速
#define DIRC1 43 
#define DIRC2 42  //C电机方向
#define PWMD 5    //D电机转速
#define DIRD1 A4  //26  
#define DIRD2 A5  //27  //D电机方向


#define left_IR_1  A3
#define left_IR_2  A1
#define Center_IR  A2
#define Right_IR1  A0
#define Right_IR2  A6
//------------------------------------------
//电机控制
//实现简单的五路巡线功能
//红外传感器
//------------------------------------------

//电机驱动类(暂时未使用)
class motor_c
{
  enum control_status
  {
    control_stop,
    control_run,
    control_backoff
  };
    uint8_t Motor_pwm;
    uint8_t control_A;
    uint8_t control_B;
    uint8_t control_PWM;
    void Motor_direction(uint8_t dir);
    void Motor_Init(uint8_t Pin_A, uint8_t Pin_B, uint8_t Pin_PWM);
  };

void motor_c::Motor_Init(uint8_t Pin_A, uint8_t Pin_B, uint8_t Pin_PWM)
{
    control_A = Pin_A;
    control_B = Pin_B;
    control_PWM = Pin_PWM;
    pinMode(control_A, OUTPUT);
    pinMode(control_B, OUTPUT);
    pinMode(control_PWM, OUTPUT);
}

void motor_c::Motor_direction(uint8_t dir)
{
  digitalWrite(control_A,LOW);
  digitalWrite(control_B,LOW);
  switch(dir)
  {
    case control_stop:    digitalWrite(control_A,LOW);  digitalWrite(control_B,LOW);  break;
    case control_run:     digitalWrite(control_A,HIGH); digitalWrite(control_B,LOW); break;
    case control_backoff: digitalWrite(control_A,LOW);  digitalWrite(control_B,HIGH); break;
    default: break;
  }
  analogWrite(control_PWM,Motor_pwm);
}

motor_c MOTOR_A;
motor_c MOTOR_B;
motor_c MOTOR_C;
motor_c MOTOR_D;
//电机驱动类


//电机控制，前进、后退、停止
#define MOTORA_FORWARD(pwm)    do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,HIGH);analogWrite(PWMA,pwm);}while(0)
#define MOTORA_STOP(x)         do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,LOW); analogWrite(PWMA,0);}while(0)
#define MOTORA_BACKOFF(pwm)    do{digitalWrite(DIRA1,HIGH);digitalWrite(DIRA2,LOW); analogWrite(PWMA,pwm);}while(0)

#define MOTORB_FORWARD(pwm)    do{digitalWrite(DIRB1,HIGH); digitalWrite(DIRB2,LOW);analogWrite(PWMB,pwm);}while(0)
#define MOTORB_STOP(x)         do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,LOW); analogWrite(PWMB,0);}while(0)
#define MOTORB_BACKOFF(pwm)    do{digitalWrite(DIRB1,LOW);digitalWrite(DIRB2,HIGH); analogWrite(PWMB,pwm);}while(0)

#define MOTORC_FORWARD(pwm)    do{digitalWrite(DIRC1,HIGH); digitalWrite(DIRC2,LOW);analogWrite(PWMC,pwm);}while(0)
#define MOTORC_STOP(x)         do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,LOW); analogWrite(PWMC,0);}while(0)
#define MOTORC_BACKOFF(pwm)    do{digitalWrite(DIRC1,LOW);digitalWrite(DIRC2,HIGH); analogWrite(PWMC,pwm);}while(0)

#define MOTORD_FORWARD(pwm)    do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,HIGH);analogWrite(PWMD,pwm);}while(0)
#define MOTORD_STOP(x)         do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,LOW); analogWrite(PWMD,0);}while(0)
#define MOTORD_BACKOFF(pwm)    do{digitalWrite(DIRD1,HIGH);digitalWrite(DIRD2,LOW); analogWrite(PWMD,pwm);}while(0)

#define SERIAL  Serial

//#define SERIAL  Serial3

#define LOG_DEBUG

#ifdef LOG_DEBUG
#define M_LOG SERIAL.print
#else
#define M_LOG 
#endif

//PWM参数
#define MAX_PWM   200
#define MIN_PWM   130

int Motor_PWM = 50;

//控制电机运动    宏定义
//    ↑A-----B↑   
//     |  ↑  |
//     |  |  |
//    ↑C-----D↑
void ADVANCE(uint8_t pwm_A,uint8_t pwm_B,uint8_t pwm_C,uint8_t pwm_D)
{
  MOTORA_FORWARD(pwm_A);MOTORB_FORWARD(pwm_B);    
  MOTORC_FORWARD(pwm_C);MOTORD_FORWARD(pwm_D);    
}

//    ↓A-----B↓ 
//     |  |  |
//     |  ↓  |
//    ↓C-----D↓
void BACK()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
//    =A-----B↑   
//     |   ↖ |
//     | ↖   |
//    ↑C-----D=
void LEFT_1()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_FORWARD(Motor_PWM);
}

//    ↓A-----B↑   
//     |  ←  |
//     |  ←  |
//    ↑C-----D↓
void LEFT_2()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_FORWARD(Motor_PWM);
  MOTORC_FORWARD(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
//    ↓A-----B=   
//     | ↙   |
//     |   ↙ |
//    =C-----D↓
void LEFT_3()
{
  MOTORA_BACKOFF(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_BACKOFF(Motor_PWM);
}
//    ↑A-----B=   
//     | ↗   |
//     |   ↗ |
//    =C-----D↑
void RIGHT_1()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_FORWARD(Motor_PWM);
}
//    ↑A-----B↓   
//     |  →  |
//     |  →  |
//    ↓C-----D↑
void RIGHT_2()
{
  MOTORA_FORWARD(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_FORWARD(Motor_PWM);
}
//    =A-----B↓   
//     |   ↘ |
//     | ↘   |
//    ↓C-----D=
void RIGHT_3()
{
  MOTORA_STOP(Motor_PWM);MOTORB_BACKOFF(Motor_PWM);
  MOTORC_BACKOFF(Motor_PWM);MOTORD_STOP(Motor_PWM);
}

//    ↑A-----B↓   
//     | ↗ ↘ |
//     | ↖ ↙ |
//    ↑C-----D↓
void rotate_1(uint8_t pwm_A,uint8_t pwm_B,uint8_t pwm_C,uint8_t pwm_D)
{
  MOTORA_BACKOFF(pwm_A);MOTORB_FORWARD(pwm_B);
  MOTORC_FORWARD(pwm_C);MOTORD_BACKOFF(pwm_D);
}

//    ↓A-----B↑   
//     | ↙ ↖ |
//     | ↘ ↗ |
//    ↓C-----D↑
void rotate_2(uint8_t pwm_A,uint8_t pwm_B,uint8_t pwm_C,uint8_t pwm_D)
{
  MOTORA_FORWARD(pwm_A);MOTORB_BACKOFF(pwm_B);
  MOTORC_BACKOFF(pwm_C);MOTORD_FORWARD(pwm_D);
}
//    =A-----B=  
//     |  =  |
//     |  =  |
//    =C-----D=
void STOP()
{
  MOTORA_STOP(Motor_PWM);MOTORB_STOP(Motor_PWM);
  MOTORC_STOP(Motor_PWM);MOTORD_STOP(Motor_PWM);
}

//串口输入控制
void UART_Control()
{
  char Uart_Date=0;
  if(SERIAL.available())
  {
    Uart_Date = SERIAL.read();
  }
  switch(Uart_Date)
  {
     case 'A':  ADVANCE(120,120,120,120);  M_LOG("Run!\r\n");        break;
     case 'B':  RIGHT_1();  M_LOG("Right up!\r\n");     break;
     case 'C':  RIGHT_2();  M_LOG("Right!\r\n");        break;
     case 'D':  RIGHT_3();  M_LOG("Right down!\r\n");   break;
     case 'E':  BACK();     M_LOG("Run!\r\n");        break;
     case 'F':  LEFT_3();   M_LOG("Left down!\r\n");    break;
     case 'G':  LEFT_2();   M_LOG("Left!\r\n");       break;
     case 'H':  LEFT_1();   M_LOG("Left up!\r\n");  break;
     case 'Z':  STOP();     M_LOG("Stop!\r\n");       break;
     case 'L':  Motor_PWM = 240;                      break;
     case 'M':  Motor_PWM = 130;                       break;
   }
}

void IO_init()
{
	pinMode(PWMA, OUTPUT);
	pinMode(DIRA1, OUTPUT);pinMode(DIRA2, OUTPUT);
	pinMode(PWMB, OUTPUT);
	pinMode(DIRB1, OUTPUT);pinMode(DIRB2, OUTPUT);
  pinMode(PWMC, OUTPUT);
	pinMode(DIRC1, OUTPUT);pinMode(DIRC2, OUTPUT);
	pinMode(PWMD, OUTPUT);
	pinMode(DIRD1, OUTPUT);pinMode(DIRD2, OUTPUT);
	STOP();
}

void setup()
{
	SERIAL.begin(115200);
	IO_init();
  SERIAL.print("Start");
}

//红外传感器检测
uint8_t center,right1,left1,right2,left2;
uint8_t motor_run;
uint8_t err_status;

void loop()
{
    UART_Control();//串口接收处理 
    //CAR_Control();//小车控制
    right1 = digitalRead(Right_IR1);
    right2 = digitalRead(Right_IR2);
    center = digitalRead(Center_IR);
    left1 = digitalRead(left_IR_1);
    left2 = digitalRead(left_IR_2);
    motor_run |= right1 << 4;
    motor_run |= right2 << 3;
    motor_run |= center << 2;
    motor_run |= left1 << 1;
    motor_run |= left2 << 0;
//电机方向调整
  switch(motor_run)
  {
     case 0x01:ADVANCE(50,140,140,50); err_status = 0x20; break;
     case 0x02:ADVANCE(50,120,120,50); err_status = 0;    break;
     case 0x06:ADVANCE(80,120,120,80);  err_status = 0;    break;
     case 0x04:ADVANCE(120,120,120,120);err_status = 0;     break;
     case 0x0C:ADVANCE(120,80,80,120); err_status = 0;    break;
     case 0x08:ADVANCE(120,50,50,120); err_status = 0;    break;
     case 0x10:ADVANCE(140,50,50,140); err_status = 0x40;break;

     case 31:   STOP(); break;
     case 0:    STOP(); break;
     default: break;
  }
  motor_run = 0;
//异常状态
  if(err_status == 0x20)
     ADVANCE(20,80,80,20);
  else if(err_status == 0x40)
     ADVANCE(80,20,20,80);
}
