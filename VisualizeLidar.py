import cv2
import time
import math

import numpy as np

import threading as thread

class VisualizeLidar():
  eraseCount = 10
  def __init__(self, canvasH: int=400, canvasW: int=400):
    self.canvasH, self.canvasW = canvasH, canvasW
    self.canvas = np.zeros((canvasW, canvasH, 3), np.uint8)
    self.lidarResults = dict()


  def toCartesian(self, angle_deg: float, distance: float):
    SCALE_FACTOR = 15
    angle_rad = (angle_deg - 90) * (math.pi / 180)
    x = ((distance / SCALE_FACTOR) * math.cos(angle_rad)) + (self.canvasW / 2)
    y = ((distance / SCALE_FACTOR) * math.sin(angle_rad)) + (self.canvasH / 2)
    return int(x), int(y)

  def eraseBackground(self, color: tuple=(0, 0, 0)):
    self.canvas.fill(0)
    self.drawCenterPoint()
    self.drawLidarHeading()
  
  def drawCenterPoint(self, color: tuple=(125, 125, 0)):
    center = (int(self.canvasW / 2), int(self.canvasH / 2))
    cv2.circle(self.canvas, center, 5, color, -1)

  def drawLidarHeading(self, color: tuple=(0, 255, 0)):
    center = (int(self.canvasW / 2), int(self.canvasH / 2))
    endPoint = self.toCartesian(0, 8000)
    cv2.line(self.canvas, center, endPoint, color, 1)

  def drawPoints(self):
    if self.lidarResults == None:
      return
    if self.eraseCount > 3:
      self.eraseBackground()
      self.eraseCount = 0
    for angle, distance in self.lidarResults.items():
      self.drawPoint(angle, distance)

    cv2.imshow('lidar', self.canvas)

    self.eraseCount += 1

  def drawPoint(self, angle: str, distance: float, color: tuple=(255, 255, 255)):
    if distance > 8000 and distance < 100:
      return
    if distance != 0:
      angle, distance = float(angle), float(distance)
      x, y = self.toCartesian(angle, distance)
      if x > 0 and x < self.canvasW and y > 0 and y < self.canvasH:
        center = (int(x), int(y))
        cv2.circle(self.canvas, center, 1, color, 1)

  def updateResults(self, lidarResults: dict):
    self.lidarResults = lidarResults

import YDLidar_3 as YDLidar

lidar = YDLidar.LidarX2("COM3", 1000)
visualizeLidar = VisualizeLidar(800, 800)

with lidar as Lidar:
  time.sleep(1)
  while True:
    time.sleep(0.01)
    results = lidar.getResutls()
    visualizeLidar.updateResults(results)
    visualizeLidar.drawPoints()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      print(results)
      break

# import LidarX2_copy as LidarX2

# Lidar = LidarX2.LidarX2()
# visualizeLidar = VisualizeLidar(800, 800)

# with Lidar as lidar:
#   time.sleep(1)
#   while True:
#     results = lidar.getMeasures()
#     visualizeLidar.updateResults(results)
#     visualizeLidar.drawPoints()
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#       break

# cv2.destroyAllWindows()

# from LidarX2_2 import LidarX2
# from VisualizeLidar import VisualizeLidar
# from threading import Thread

# lidarX2 = LidarX2("COM3")
# visualizeLidar = VisualizeLidar(800, 800)

# lidarX2.Connect()

# measure_thread = Thread(target=lidarX2.getMeasures)
# measure_thread.start()
# measure_thread.join()
# while True:
#   # print(lidarX2.measureList)
#   visualizeLidar.updateResults(lidarX2.measureList)
#   visualizeLidar.drawPoints()
#   if cv2.waitKey(1) & 0xFF == ord('q'):
#       break