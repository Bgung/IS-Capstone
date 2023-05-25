#include <I2Cdev.h>

#include <MPU6050.h>
#include <MPU6050_6Axis_MotionApps20.h>
#include <MPU6050_9Axis_MotionApps41.h>
#include <helper_3dmath.h>


MPU6050 mpu;

uint8_t devStatus;

void setup(){
  Serial.begin(115200);

  mpu.initialize()

  Serial.println(F("Testing device connections..."));
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

  devStatus = mpu.dmpInitialize();

  
  mpu.setDMPEnabled(true);
}

void loop(){
  
}