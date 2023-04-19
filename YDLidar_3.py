import math

import numpy as np

from serial import Serial #pip install pySerial
from time import sleep
from math import atan, pi
from threading import Thread, Lock

from dataclasses import dataclass
from typing import Union

@dataclass
class LidarMeasure:
  def __init__(self, angle, distance):
    self.angle = angle
    self.distance = distance
  def __repr__(self):
    return {"Angle": self.angle, "Distance": self.distance}.__str__()
  

class LidarX2:
  def __init__(self, port: str="COM3", chunkSize: int = 2000):
    self._port = port
    self._chunkSize = chunkSize
    self._is_connected = False
    self._max_distance = 10000
    self._LOCK = Lock()
    self._results = dict()

  def __enter__(self):
    self.__open__()
    self._startScan()
    return self

  def __open__(self):
    if self._is_connected:
      return True
    try:
      self.serial = Serial(
        port=self._port,
        baudrate=115200,
        timeout=1
      )
      self._is_connected = True
    except Exception as e:
      print(e)
      self._is_connected = False
    return self._is_connected

  def _startScan(self):
    if self._is_connected:
      self._last_chunk = None
      self._scanThread = Thread(target=self._scan, args=())
      self._scanThread.isDaemon = True
      self._scanThread.start()
      return True
    return False
  
  def _endScan(self):
    if self._is_connected:
      self._scanThread.join()
      self._scanThread = None
      self._last_chunk = None
      return True
    return False

  def __exit__(self, exc_type, exc_val, exc_tb):
    print("Exception: ", exc_type, exc_val, exc_tb)
    self._endScan()
    self.serial.close()
    self._is_connected = False

  def _getAngleCorrection(self, dist):
    if dist != 0:
      return math.atan(21.8 * ((155.3 - dist) / (155.3 * dist)))
    return 0

  def _getAngleDiff(self, startAngle, endAngle):
    angleDiff = endAngle - startAngle
    if startAngle > endAngle:
      return 360 - angleDiff
    else:
      return angleDiff

  def _scan(self):
    while True:
      dataBlocks = self.serial.read(self._chunkSize).split(b'\xaa\x55')
      if self._last_chunk is not None:
        dataBlocks[0] = self._last_chunk + dataBlocks[0]
      self._last_chunk = dataBlocks.pop()

      for dataBlock in dataBlocks:
        self._analysisDataBlock(dataBlock)
      self._cleanResults()
  
  # Analysis each data block
  def _analysisDataBlock(self, dataBlock):
    lenOfDataBlock = len(dataBlock)
    # print(lenOfDataBlock)
    if lenOfDataBlock < 10:
      # Reasonable length of the data slice?
      return list()
    
    # Get sample count and start and end angle
    sampleCount = dataBlock[1]
    if sampleCount == 0 or sampleCount == 1:
      # If sample count is 0 return list which length == 0
      return list()
    
    # Distance analysis
    distances = list()
    for i in range(8, lenOfDataBlock - 1, 2):
      dist = round((dataBlock[i] + 256 * dataBlock[i + 1]) / 4)
      distances.append(dist)
    
    # First-level analysis
    startAngle = ((dataBlock[2] + 256 * dataBlock[3]) >> 1) / 64
    endAngle = ((dataBlock[4] + 256 * dataBlock[5]) >> 1) / 64
    angleDiff = self._getAngleDiff(startAngle, endAngle)
    firstAnalysis = list()
    for i in range(2, sampleCount + 2, 1):
      angle_i = ((angleDiff * (i - 1)) / (sampleCount - 1)) + startAngle
      firstAnalysis.append(angle_i)
    
    # Second-level analysis
    angleCorrections = list()
    for distance in distances:
      angleCorrection = self._getAngleCorrection(distance)
      angleCorrections.append(angleCorrection)

    # Intergrate analysis
    # print(len(firstAnalysis), len(angleCorrections), len(distances))
    for angle_i, angleCorrection_i, distance_i in zip(firstAnalysis, angleCorrections, distances):
      angle = round(angle_i + angleCorrection_i)
      distance = round(distance_i, 4)
      if angle >= 360:
        angle -= 360

      if angle >= 0 and angle < 360:
        self._results[str(angle)] = distance

  def _cleanResults(self):
    self._LOCK.acquire()
    for key in list(self._results.keys()):
      key = float(key)
      if key > 360 or key < 0:
        print("Delete key: ", key, " value: ", self._results[key])
        del self._results[key]
    # if len(self._results.keys()) > 999:
    #   print("Clrear results")
    #   self._results = dict()
    self._LOCK.release()

  def getResutls(self) -> dict:
    self._LOCK.acquire()
    results = self._results.copy()
    self._LOCK.release()
    return results
