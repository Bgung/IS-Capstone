import cv2
import time
import math

import numpy as np

from typing import Tuple

class VisualizeLidar():
  eraseCount = 10
  def __init__(self, canvasH: int=400, canvasW: int=400):
    self.canvasH, self.canvasW = canvasH, canvasW
    self.canvas = np.zeros((canvasW, canvasH, 3), np.uint8)
    self.canvasCenter = (int(canvasW / 2), int(canvasH / 2))
    self.lidarPolarResults = dict()
    self.SCALE_FACTOR = 30

  def toCartesian(self, angle_deg: float, distance: float):
    angle_rad = (angle_deg + 90) * (math.pi / 180)
    x = ((distance / self.SCALE_FACTOR) * math.cos(angle_rad))
    y = ((distance / self.SCALE_FACTOR) * math.sin(angle_rad))
    return int(x), int(y)

  def eraseBackground(self, color: tuple=(50, 150, 0)):
    for c in range(3):
      self.canvas[:, :, c].fill(color[c])
    self.drawCenterPoint()
    self.drawLidarHeading()
  
  def drawCenterPoint(self, color: tuple=(125, 125, 0)):
    cv2.circle(self.canvas, self.canvasCenter, 3, color, -1)

  def drawLidarHeading(self, color: tuple=(0, 255, 0)):
    point = (0 + self.canvasCenter[0], 0)
    cv2.line(self.canvas, self.canvasCenter, point, color, 1)

  def drawPolarPoints(self):
    if self.lidarPolarResults == None:
      return
    if self.eraseCount > 5:
      self.eraseBackground()
      self.eraseCount = 0
    for angle, distance in self.lidarPolarResults.items():
      self.drawPolarPoint(angle, distance)

    cv2.imshow('lidar', self.canvas)

    self.eraseCount += 1

  def drawCartesianPoints(self):
    if self.eraseCount > 1:
      self.eraseBackground()
      self.eraseCount = 0
    for point in self.lidarCartesianResults:
      self.drawCartesianPoint(point)

    cv2.imshow('lidar', self.canvas)

    self.eraseCount += 1


  def drawPolarPoint(self, angle: str, distance: str, color: tuple=(255, 255, 255)):
    if distance != 0:
      angle, distance = float(angle), float(distance)
      x, y = self.toCartesian(angle, distance)
      self.drawCartesianPoint(x, y, color)

  def drawCartesianPoint(self, x: int, y: int, color: tuple=(255, 255, 255)):
    x, y = (int(x + self.canvasCenter[0]), int(y + self.canvasCenter[1]))
    self.drawPoint(x, y, color)

  def drawPoint(self, x: int, y: int, color: tuple=(255, 255, 255)):
    if x > 0 and x < self.canvasW and y > 0 and y < self.canvasH:
      cv2.circle(self.canvas, (x, y), 3, color, -1)

  def updatePolarResults(self, lidarResults: dict):
    self.lidarPolarResults = lidarResults

  def updateCartesianResults(self, lidarResults: list):
    self.lidarCartesianResults = lidarResults

import YDLidarX2 as YDLidar

lidar = YDLidar.LidarX2("COM3", 500)
visualizeLidar = VisualizeLidar(800, 800)

with lidar as Lidar:
  time.sleep(1)
  while True:
    polarResults = lidar.getPolarResults()
    visualizeLidar.updatePolarResults(polarResults)
    visualizeLidar.drawPolarPoints()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
