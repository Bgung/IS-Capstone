//三传感器
//正前超声波传感器A引脚定义
#define Echo_A 22//超声波接收端引脚
#define Trig_A 24//超声波控制端引脚
//左前超声波传感器B引脚定义
#define Echo_B 47//超声波接收端引脚
#define Trig_B 48//超声波控制端引脚
//右前超声波传感器C引脚定义
#define Echo_C 28 //超声波接收端引脚
#define Trig_C 25//超声波控制端引脚

//电机引脚定义
#define PWMA 12    //A电机转速
#define DIRA1 34 
#define DIRA2 35  //A电机方向
#define PWMB 8    //B电机转速
#define DIRB1 37 
#define DIRB2 36  //B电机方向
#define PWMC 9   //C电机转速
#define DIRC1 43 
#define DIRC2 42  //C电机方向
#define PWMD 5    //D电机转速
#define DIRD1 A4  
#define DIRD2 A5  //D电机方向

//电机控制，前进、后退、停止
//左前轮
#define MOTORA_FORWARD(pwm)    do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,HIGH);analogWrite(PWMA,pwm);}while(0)
#define MOTORA_STOP(x)         do{digitalWrite(DIRA1,LOW); digitalWrite(DIRA2,LOW); analogWrite(PWMA,0);}while(0)
#define MOTORA_BACKOFF(pwm)    do{digitalWrite(DIRA1,HIGH);digitalWrite(DIRA2,LOW); analogWrite(PWMA,pwm);}while(0)
//右前轮
#define MOTORB_FORWARD(pwm)    do{digitalWrite(DIRB1,HIGH); digitalWrite(DIRB2,LOW);analogWrite(PWMB,pwm);}while(0)
#define MOTORB_STOP(x)         do{digitalWrite(DIRB1,LOW); digitalWrite(DIRB2,LOW); analogWrite(PWMB,0);}while(0)
#define MOTORB_BACKOFF(pwm)    do{digitalWrite(DIRB1,LOW);digitalWrite(DIRB2,HIGH); analogWrite(PWMB,pwm);}while(0)
//左后轮
#define MOTORC_FORWARD(pwm)    do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,HIGH);analogWrite(PWMC,pwm);}while(0)
#define MOTORC_STOP(x)         do{digitalWrite(DIRC1,LOW); digitalWrite(DIRC2,LOW); analogWrite(PWMC,0);}while(0)
#define MOTORC_BACKOFF(pwm)    do{digitalWrite(DIRC1,HIGH);digitalWrite(DIRC2,LOW); analogWrite(PWMC,pwm);}while(0)
//右后轮
#define MOTORD_FORWARD(pwm)    do{digitalWrite(DIRD1,HIGH); digitalWrite(DIRD2,LOW);analogWrite(PWMD,pwm);}while(0)
#define MOTORD_STOP(x)         do{digitalWrite(DIRD1,LOW); digitalWrite(DIRD2,LOW); analogWrite(PWMD,0);}while(0)
#define MOTORD_BACKOFF(pwm)    do{digitalWrite(DIRD1,LOW);digitalWrite(DIRD2,HIGH); analogWrite(PWMD,pwm);}while(0)


#define SERIAL  Serial

//PWM参数定义
#define MAX_PWM   200
#define MIN_PWM   130

int Motor_PWM =80;
int Motor_PWM_LOW =70;
int Motor_PWM_HIGH =100;

//控制电机运动    宏定义

//    ↑A-----B↑   
//     |  ↑  |
//     |  |  |
//    ↑C-----D↑
void ADVANCE()
{
  MOTORA_FORWARD(Motor_PWM_HIGH);MOTORB_FORWARD(Motor_PWM_HIGH);    
  MOTORC_FORWARD(Motor_PWM_HIGH);MOTORD_FORWARD(Motor_PWM_HIGH);    
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
  MOTORA_BACKOFF(Motor_PWM_LOW);MOTORB_FORWARD(Motor_PWM_LOW);
  MOTORC_FORWARD(Motor_PWM_LOW);MOTORD_BACKOFF(Motor_PWM_LOW);
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
  MOTORA_FORWARD(Motor_PWM_LOW);MOTORB_BACKOFF(Motor_PWM_LOW);
  MOTORC_BACKOFF(Motor_PWM_LOW);MOTORD_FORWARD(Motor_PWM_LOW);
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

//初始化距离数据
float echoDistance_A;
float echoDistance_B;
float echoDistance_C;
int leftDistance = 0;
int rightDistance = 0;
int forwardDistance = 0;

#define LOG_DEBUG

#ifdef LOG_DEBUG
#define M_LOG SERIAL.print
#else
#define M_LOG 
#endif



void IO_init()//引脚模式定义
{
  pinMode(PWMA, OUTPUT);
  pinMode(DIRA1, OUTPUT);pinMode(DIRA2, OUTPUT);
  pinMode(PWMB, OUTPUT);
  pinMode(DIRB1, OUTPUT);pinMode(DIRB2, OUTPUT);
  pinMode(PWMC, OUTPUT);
  pinMode(DIRC1, OUTPUT);pinMode(DIRC2, OUTPUT);
  pinMode(PWMD, OUTPUT);
  pinMode(DIRD1, OUTPUT);pinMode(DIRD2, OUTPUT);
  pinMode(Trig_A,OUTPUT);
  pinMode(Echo_A,INPUT);
pinMode(Trig_B,OUTPUT);
  pinMode(Echo_B,INPUT);
pinMode(Trig_C,OUTPUT);
  pinMode(Echo_C,INPUT);
  STOP();
}

int testDistance_A(){//测距子程序
  //激发超声波模块
  digitalWrite(Trig_A,LOW);
  delayMicroseconds(2);
  digitalWrite(Trig_A,HIGH);
  delayMicroseconds(20);
  digitalWrite(Trig_A,LOW);
  echoDistance_A = pulseIn(Echo_A,HIGH);
  echoDistance_A /= 58;// echoDistance= echoDistance÷58
  return (int)echoDistance_A;
}
int testDistance_B(){//测距子程序
  //激发超声波模块
  digitalWrite(Trig_B,LOW);
  delayMicroseconds(2);
  digitalWrite(Trig_B,HIGH);
  delayMicroseconds(20);
  digitalWrite(Trig_B,LOW);
  echoDistance_B = pulseIn(Echo_B,HIGH);
  echoDistance_B /= 58;// echoDistance= echoDistance÷58
  return (int)echoDistance_B;
}
int testDistance_C(){//测距子程序
  //激发超声波模块
  digitalWrite(Trig_C,LOW);
  delayMicroseconds(2);
  digitalWrite(Trig_C,HIGH);
  delayMicroseconds(20);
  digitalWrite(Trig_C,LOW);
  echoDistance_C = pulseIn(Echo_C,HIGH);
  echoDistance_C /= 58;// echoDistance= echoDistance÷58
  return (int)echoDistance_C;
}

void setup()
{
  SERIAL.begin(9600);
IO_init();
}

void loop()
{    forwardDistance = testDistance_A();//储存前方距离测得数据
leftDistance = testDistance_B();//储存前方距离测得数据
rightDistance = testDistance_C();//储存前方距离测得数据

if ( forwardDistance<=30) { 
if(leftDistance<=30) {
  RIGHT_2();
  
  M_LOG("左、前方有障碍物，向右平移\r\n");
}
else{
 LEFT_2();
 M_LOG("右、前方有障碍物，向左平移\r\n");
}
} 
else if(leftDistance<=30) { 
RIGHT_2();
M_LOG("左侧有障碍物，向右平移\r\n");
} 
else if(rightDistance<=30) { 
LEFT_2();
M_LOG("右侧有障碍物，向左平移!\r\n");
} 
else { 
ADVANCE(); 
M_LOG("前进\r\n");
}
}
