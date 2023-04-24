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
    self.canvasCenter = (int(canvasW / 2), int(canvasH / 2))
    self.lidarPolarResults = dict()

  def toCartesian(self, angle_deg: float, distance: float):
    SCALE_FACTOR = 15
    angle_rad = (angle_deg - 90) * (math.pi / 180)
    x = ((distance / SCALE_FACTOR) * math.cos(angle_rad)) + self.canvasCenter[0]
    y = ((distance / SCALE_FACTOR) * math.sin(angle_rad)) + self.canvasCenter[1]
    return int(x), int(y)

  def eraseBackground(self, color: tuple=(0, 0, 0)):
    self.canvas.fill(0)
    self.drawCenterPoint()
    self.drawLidarHeading()
  
  def drawCenterPoint(self, color: tuple=(125, 125, 0)):
    cv2.circle(self.canvas, self.canvasCenter, 3, color, -1)

  def drawLidarHeading(self, color: tuple=(0, 255, 0)):
    endPoint = self.toCartesian(0, 8000)
    cv2.line(self.canvas, self.canvasCenter, endPoint, color, 1)

  def drawPoints(self):
    if self.lidarPolarResults == None:
      return
    if self.eraseCount > 1:
      self.eraseBackground()
      self.eraseCount = 0
    for angle, distance in self.lidarPolarResults.items():
      self.drawPoint(angle, distance)

    cv2.imshow('lidar', self.canvas)

    self.eraseCount += 1

  def drawPoint(self, angle: str, distance: str, color: tuple=(255, 255, 255)):
    if distance != 0:
      angle, distance = float(angle), float(distance)
      x, y = self.toCartesian(angle, distance)
      if x > 0 and x < self.canvasW and y > 0 and y < self.canvasH:
        point = (int(x), int(y))
        cv2.circle(self.canvas, point, 1, color, -1)

  def updatePolarResults(self, lidarResults: dict):
    self.lidarPolarResults = lidarResults

import YDLidarX2 as YDLidar

lidar = YDLidar.LidarX2("COM3", 500)
visualizeLidar = VisualizeLidar(800, 800)

with lidar as Lidar:
  time.sleep(1)
  while True:
    # time.sleep(0.01)
    polarResults = lidar.getPolarResults()
    visualizeLidar.updatePolarResults(polarResults)
    visualizeLidar.drawPoints()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      print(polarResults)
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