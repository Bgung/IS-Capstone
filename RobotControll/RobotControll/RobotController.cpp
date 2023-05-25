#include <Arduino.h>

#include "RobotController.hpp"
#include "RobotControllerConstant.hpp"

#ifndef PINMAP

#define PWMA 4
#define DIRA1 A4
#define DIRA2 A5

#define PWMB 6
#define DIRB1 43
#define DIRB2 42

#define PWMC 11
#define DIRC1 34
#define DIRC2 35

#define PWMD 7
#define DIRD1 37
#define DIRD2 36

#define FORWARD 1
#define BACKWARD 0

#define PINMAP
#endif

RobotController::RobotController() {
    pinMode(PWMA, OUTPUT);
    pinMode(PWMB, OUTPUT);
    pinMode(PWMC, OUTPUT);
    pinMode(PWMD, OUTPUT);

    pinMode(DIRA1, OUTPUT);
    pinMode(DIRA2, OUTPUT);
    pinMode(DIRB1, OUTPUT);
    pinMode(DIRB2, OUTPUT);
    pinMode(DIRC1, OUTPUT);
    pinMode(DIRC2, OUTPUT);
    pinMode(DIRD1, OUTPUT);
    pinMode(DIRD2, OUTPUT);
}

void RobotController::driveMotor(unsigned int motor, unsigned int dir) {
    if(motor == this->MOTOR_FL) {
        digitalWrite(DIRA1, dir);
        digitalWrite(DIRA2, !dir);
        analogWrite(PWMA, this->cur_speed);
    } else if(motor == this->MOTOR_FR) {
        digitalWrite(DIRB1, dir);
        digitalWrite(DIRB2, !dir);
        analogWrite(PWMB, this->cur_speed);
    }
    if(motor == this->MOTOR_BL) {
        digitalWrite(DIRC1, 1);
        digitalWrite(DIRC2, 0);
        analogWrite(PWMC, this->cur_speed);
    } else if(motor == this->MOTOR_BR) {
        digitalWrite(DIRD1, 1);
        digitalWrite(DIRD2, 0);
        analogWrite(PWMD, this->cur_speed);
    }
}

void RobotController::forward() {
    this->driveMotor(
      this->MOTOR_FL,
      FORWARD
    );
    this->driveMotor(
      this->MOTOR_FR,
      FORWARD
    );
    this->driveMotor(
      this->MOTOR_BL,
      FORWARD
    );
    this->driveMotor(
      this->MOTOR_BR,
      FORWARD
    );
}

void RobotController::backward() {
    this->driveMotor(
      this->MOTOR_FL,
      BACKWARD
    );
    this->driveMotor(
      this->MOTOR_FR,
      BACKWARD
    );
    this->driveMotor(
      this->MOTOR_BL,
      BACKWARD
    );
    this->driveMotor(
      this->MOTOR_BR,
      BACKWARD
    );
}

void RobotController::right(unsigned int power) {
    this->driveMotor(
      this->MOTOR_FL,
      FORWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_FR,
      BACKWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_BL,
      FORWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_BR,
      BACKWARD,
      power
    );
}

void RobotController::left(unsigned int power) {
    this->driveMotor(
      this->MOTOR_FL,
      BACKWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_FR,
      FORWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_BL,
      BACKWARD,
      power
    );
    this->driveMotor(
      this->MOTOR_BR,
      FORWARD,
      power
    );
}

void RobotController::stop() {
    this->stopMotor(this->MOTOR_FL);
    this->stopMotor(this->MOTOR_FR);
    this->stopMotor(this->MOTOR_BL);
    this->stopMotor(this->MOTOR_BR);
}

void RobotController::stopMotor(unsigned int motor) {
    this->driveMotor(motor, FORWARD, 0);
}

void RobotController::setSpeedAndDirection(unsigned int speed, float direction) {
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

void RobotController::setIsInterrupted(bool isInterrupted) {
    this->isInterrupted = isInterrupted;
}

bool RobotController::getIsInterrupted() {
    return this->isInterrupted;
}