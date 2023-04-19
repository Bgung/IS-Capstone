class RobotState {
private:
  
}

class RobotController {
private:
    unsigned int speed = 100;
    unsigned char direction = 0;
public:
    RobotController();
    void driveArdumoto(unsigned int motor, unsigned int dir, unsigned int speed);
    void stopArdumoto(unsigned int motor);
    void forward(unsigned char velocity);
    void backward(unsigned char velocity);
    void right(unsigned char velocity);
    void left(unsigned char velocity);
    void setSpeedAndDirection(float speed, float direction);
    void stop();
};

