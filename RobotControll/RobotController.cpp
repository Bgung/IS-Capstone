#include <Arduino.h>

#include "RobotController.hpp"

namespace RobotControllerConstant{
    unsigned int PWMA = 3;
    unsigned int PWMB = 11;
    unsigned int DIRA = 12;
    unsigned int DIRB = 13;

    unsigned int MOTOR_LEFT = 0;
    unsigned int MOTOR_RIGHT = 1;

    unsigned int CW = 1;
    unsigned int CCW = 0;

    unsigned int DEFAULT_POWER = 100;
    unsigned int MAX_POWER = 255;
}

RobotController::RobotController() {
    pinMode(RobotControllerConstant::PWMA, OUTPUT);
    pinMode(RobotControllerConstant::PWMB, OUTPUT);
    pinMode(RobotControllerConstant::DIRA, OUTPUT);
    pinMode(RobotControllerConstant::DIRB, OUTPUT);

    digitalWrite(RobotControllerConstant::PWMA, LOW);
    digitalWrite(RobotControllerConstant::PWMB, LOW);
    digitalWrite(RobotControllerConstant::DIRA, LOW);
    digitalWrite(RobotControllerConstant::DIRB, LOW);
}

void RobotController::forward(unsigned char velocity) {
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_LEFT,
      RobotControllerConstant::CW,
      velocity
    );
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_RIGHT,
      RobotControllerConstant::CCW,
      velocity
    );
}

void RobotController::backward(unsigned char velocity) {
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_LEFT,
      RobotControllerConstant::CCW,
      velocity
    );
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_RIGHT,
      RobotControllerConstant::CW,
      velocity
    );
}

void RobotController::right(unsigned char velocity) {
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_LEFT,
      RobotControllerConstant::CCW,
      velocity
    );
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_RIGHT,
      RobotControllerConstant::CCW,
      velocity
    );
}

void RobotController::left(unsigned char velocity) {
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_LEFT,
      RobotControllerConstant::CW,
      velocity
    );
    this->driveArdumoto(
      RobotControllerConstant::MOTOR_RIGHT,
      RobotControllerConstant::CW,
      velocity
    );
}

void RobotController::driveArdumoto(unsigned int motor, unsigned int dir, unsigned int spd) {
    if(motor == RobotControllerConstant::MOTOR_LEFT) {
        digitalWrite(RobotControllerConstant::DIRA, dir);
        analogWrite(RobotControllerConstant::PWMA, spd);
    } else if(motor == RobotControllerConstant::MOTOR_RIGHT) {
        digitalWrite(RobotControllerConstant::DIRB, dir);
        analogWrite(RobotControllerConstant::PWMB, spd);
    }
}

void RobotController::stopArdumoto(unsigned int motor) {
    this->driveArdumoto(motor, 0, 0);
}

void RobotController::stop() {
    this->stopArdumoto(RobotControllerConstant::MOTOR_LEFT);
    this->stopArdumoto(RobotControllerConstant::MOTOR_RIGHT);
}

void RobotController::setSpeedAndDirection(float speed, float direction) {
    if(speed == 0) {
        this->stop();
    } else if(speed > 0) {
        if(direction == 0) {
            this->forward(speed);
        } else if(direction > 0) {
            this->right(speed);
        } else if(direction < 0) {
            this->left(speed);
        }
    } else if(speed < 0) {
        if(direction == 0) {
            this->backward(speed);
        } else if(direction > 0) {
            this->left(speed);
        } else if(direction < 0) {
            this->right(speed);
        }
    }
}