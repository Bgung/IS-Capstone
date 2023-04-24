
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

