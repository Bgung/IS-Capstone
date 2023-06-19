import cv2
import time
import math

import numpy as np

from typing import Tuple, Union
from copy import copy

class VisualizeLidar():
  eraseCount = 10
  def __init__(self, canvasH: int=400, canvasW: int=400) -> None:
    self.canvasH, self.canvasW = canvasH, canvasW
    self.canvas = np.zeros((canvasW, canvasH, 3), np.uint8)
    self.canvasCenter = (int(canvasW / 2), int(canvasH / 2))
    self.lidarPolarResults = dict()
    self.lidarCartesianResults = list()
    self.SCALE_FACTOR = 30

  def toCartesian(self, angle_deg: Union[float, str], distance: float) -> Tuple[int, int]:
    '''
    Mapping polar coordinates to cartesian coordinates
    angle_deg: angle in degrees
    distance: distance in mm
    '''
    if not isinstance(angle_deg, float):
      angle_deg = float(angle_deg)
    angle_rad = (angle_deg + 90) * (math.pi / 180)
    x = ((distance / self.SCALE_FACTOR) * math.cos(angle_rad))
    y = ((distance / self.SCALE_FACTOR) * math.sin(angle_rad))
    return int(x), int(y)

  def eraseBackground(self, color: Tuple[int, int, int]=(50, 150, 0)) -> None:
    '''
    Erase the background of the canvas
    '''
    for c in range(3):
      self.canvas[:, :, c].fill(color[c])
    self.drawCenterPoint()
    self.drawLidarHeading()
  
  def drawCenterPoint(self, color: Tuple[int, int, int]=(125, 125, 0)) -> None:
    cv2.circle(self.canvas, self.canvasCenter, 3, color, -1)

  def drawLidarHeading(self, color: Tuple[int, int, int]=(0, 255, 0)) -> None:
    point = (0 + self.canvasCenter[0], 0)
    cv2.line(self.canvas, self.canvasCenter, point, color, 1)

  def drawPolarPoints(self):
    '''
    Draw the polar points on the canvas
    '''
    if self.lidarPolarResults == None:
      return
    self.eraseBackground()
    self.drawCenterPoint()
    self.drawLidarHeading()
    for angle, distance in self.lidarPolarResults.items():
      self.drawPolarPoint(angle, distance)
    self.drawLineBetweenPoint()
    cv2.imshow('lidar', self.canvas)

  def drawLineBetweenPoint(self, color: tuple=(255, 255, 255)):
    THRESHOLD = 100
    keys = list(self.lidarPolarResults.keys())
    print(len(keys))
    idx2 = 0
    for idx in range(0, 360, 1):
      if not str(idx) in keys:
        continue
      if idx == 359:
        idx2 = 0
      else:
        idx2 = idx + 1
      if not str(idx2) in keys:
        while True:
          idx2 += 1
          if str(idx2) in keys:
            break
          if idx2 > 360:
            return
      # print(idx, idx2)
      angle1, distance1 = idx, self.lidarPolarResults[str(idx)]
      angle2, distance2 = idx2, self.lidarPolarResults[str(idx2)]
      if distance1 < 100 or distance2 < 100:
        continue
      x1, y1 = self.toCartesian(angle1, distance1)
      x2, y2 = self.toCartesian(angle2, distance2)
      # if math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) > THRESHOLD:
      #   continue
      # cv2.line(
      #   self.canvas,
      #   (x1 + self.canvasCenter[0], y1 + self.canvasCenter[1]),
      #   (x2 + self.canvasCenter[0], y2 + self.canvasCenter[1]),
      #   color,
      #   3
      # )

  def drawPolarPoint(self, angle: str, distance: float, color: tuple=(255, 255, 255)):
    if distance != 0:
      angle, distance = float(angle), float(distance)
      x, y = self.toCartesian(angle, distance)
      self.drawCartesianPoint(x, y, color)

  def drawCartesianPoint(self, x: int, y: int, color: tuple=(255, 255, 255)):
    x, y = (int(x + self.canvasCenter[0]), int(y + self.canvasCenter[1]))
    if x > 0 and x < self.canvasW and y > 0 and y < self.canvasH:
      cv2.circle(self.canvas, (x, y), 1, color, -1)

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
