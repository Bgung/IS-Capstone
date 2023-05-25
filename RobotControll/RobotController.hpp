#include "Motor.hpp"


class RobotController {
  private:
    unsigned int currentSpeed = 0;
    
    Motor *motorLF = new Motor(18, 31, 11, 34, 35, true);
    Motor *motorLF = new Motor(19, 38, 7, 36, 37, false);
    Motor *motorLF = new Motor(3, 49, 6, 43, 42, true);
    Motor *motorLF = new Motor(2, A1, 4, A5, A4, false);

    bool isInterrupted = false;
  public:
    RobotController();
    void driveMotor(unsigned int motor, unsigned int dir, unsigned int spd);
    void stopMotor(unsigned int motor);
    void forward(unsigned int power);
    void backward(unsigned int power);
    void right(unsigned int power);
    void left(unsigned int power);

    void setCurrentSpeed(unsigned int currentSpeed);
    unsigned int getCurrentSpeed();

    void setSpeedAndDirection(unsigned int speed, float direction);
    void stop();
    
    void setIsInterrupted(bool isInterrupted);
    bool getIsInterrupted();
};
