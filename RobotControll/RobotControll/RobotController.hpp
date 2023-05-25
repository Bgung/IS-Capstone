class RobotController {
  private:
    unsigned int cur_speed = 0;
    
    unsigned int MOTOR_FL = 0; // Front Left
    unsigned int MOTOR_FR = 1; // Front Right
    unsigned int MOTOR_BL = 2; // Back Left
    unsigned int MOTOR_BR = 3; // Back Right
    bool isInterrupted = false;
  public:
    RobotController();
    void driveMotor(unsigned int motor, unsigned int dir, unsigned int spd);
    void stopMotor(unsigned int motor);
    void forward(unsigned int power);
    void backward(unsigned int power);
    void right(unsigned int power);
    void left(unsigned int power);
    void setSpeedAndDirection(unsigned int speed, float direction);
    void stop();
    
    void setIsInterrupted(bool isInterrupted);
    bool getIsInterrupted();
};
