# import time
# from YDLidarX2_python.LidarX2 import LidarX2

# lidar = LidarX2("COM3")  # Name of the serial port, can be /dev/tty*, COM*, etc.

# if not lidar.open():
#     print("Cannot open lidar")
#     exit(1)

# t = time.time()
# while time.time() - t < 2000:  # Run for 20 seconds
#     measures = lidar.getMeasures()  # Get latest lidar measures
#     for measure in measures:
#       print("Angle: ", measure.angle)
#       print("Distance: ", measure.distance)
#     time.sleep(1)

# lidar.close()

import PyLidar3
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty* 
port = input("Enter port name which lidar is connected:") #windows
#port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4(port) #PyLidar3.your_version_of_lidar(port,chunk_size)
Obj._baudrate = 115200
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 30: #scan for 30 seconds
        print(next(gen))
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")