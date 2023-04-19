import serial
import time
import math

from serial import Serial #pip install pySerial
from time import sleep
from math import atan, pi
from threading import Thread

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
  def __init__(self, port: int="COM3", baudrate: int="115200"):
    self.port = port
    self.baudrate = baudrate
    self.connected = False
    self.measureThread = None
    self.stopThread = False
    self.measureList = list()
    self.serial = None
    self.chunkSize = 2000

  def __open__(self):
    try:
      if self.connected:
        return True
      self.serial = Serial(
        port=self.port,
        baudrate=self.baudrate,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
      )
      TIMEOUT = 40000 # ms
      
      while not self.serial.is_open and TIMEOUT > 0:
        TIMEOUT -= 10
        sleep(0.01)
      if self.serial.is_open:
        self.connected = True
        self.serial.flush()
      else:
        return False
      
      self.stopThread = False
      self.measureThread = Thread(target=self._measureThread, args=())
      self.measureThread.isDaemon = True
      self.measureThread.start()
      return True
      
    except Exception as e:
      print(e)
    return False

  def __enter__(self):
    ret = self.__open__()
    if ret:
      return self
    else:
      raise Exception

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.stopThread = True
    if self.measureThread:
      self.measureThread.join()
    if self.connected:
      self.serial.close()
      self.connected = False
  
  def getMeasures(self):
    return list(self.measureList)
  
  def _measureThread(self):
    startAngle = 0
    while True:
      measureList = self._readMeasure()
      if len(measureList) == 0:
        self.measureList = list()
        continue
      endAngle = measureList[-1].angle

      i = 0
      while i < len(self.measureList):
        m = self.measureList[i]

        if endAngle > startAngle:
          inRange = startAngle <= m.angle and m.angle <= endAngle
        else:
          inRange = (startAngle <= m.angle and m.angle <= 360) or (0 <= m.angle and m.angle <= endAngle)
        if inRange:
          self.measureList.pop(i)
          i -= 1
        i += 1

      for m in measureList:
        self._insortMeasure(self.measureList, m)
      startAngle = endAngle

  def _insortMeasure(self, measureList, measure, lo=0, hi=None):
    if lo < 0:
      raise ValueError('lo must be non-negative')
    if hi is None:
      hi = len(measureList)
    while lo < hi:
      mid = (lo + hi) // 2
      if measureList[mid].angle < measure.angle:
        lo = mid + 1
      else:
        hi = mid
    measureList.insert(lo, measure)

  def _convert2IntDispatch(self, value):
    if isinstance(value, str):
      return self._str2Int(value)
    elif isinstance(value, bytes):
      return self._byte2Int(value)
    elif isinstance(value, int):
      return value
    
  def _readByte(self):
    value = self.serial.read(1)
    return self._convert2IntDispatch(value)

  def _str2Int(self, value):
    return int(value.encode('hex'), 16)
  
  def _byte2Int(self, value):
    return int.from_bytes(value, byteorder='little')
  
  def _readMeasure(self):
    result = list()
    if not self.connected:
      return result
    
    found = False
    checkSum = 0x55AA
    l = list()
    while not found and not self.stopThread:
      # 모든 Bytes는 0xaa가 앞에 나오고 뒤에 값이 나옴 (Little endian)
      while self.serial.read(1) == b'\xaa':
        pass
      if self.serial.read(1) == b'\x55':
        # \xaa\x55 가 나오면 데이터 한 줄의 시작을 의미
        found = True
    if self.stopThread:
      return list()
    
    # Datasheet에 있는 각각 데이터들을 읽음

    # packageType(1 byte) = 0: PointCloud data
    packageType = self._readByte()
    # if packageType != 0:
    #   return result
    # else:
    #   print('!!!!!')
    
    # sampleQuantity(1 byte) = # of sampled data
    sampleQuantity = self._readByte()
    # if sampleQuantity == 0:
    #   return result
    
    # startAngle(2 byte): degree
    startAngleL = self._readByte()
    startAngleM = self._readByte()
    F_SA, startAngle = self._calcAngle(startAngleL, startAngleM)
    checkSum ^= F_SA

    # endAngle(2 byte): degree
    endAngleL = self._readByte()
    endAngleM = self._readByte()
    L_SA, endAngle = self._calcAngle(endAngleL, endAngleM)

    # checkCode(CheckSum)(2 byte): 
    checkCodeL = self._readByte()
    checkCodeM = self._readByte()
    CC = checkCodeL
    CC += (checkCodeM << 8)

    # sampledDataRaw(sampledQuantity * 2 byte):
    # sampleQuantity = 40
    sampledDataRaw = self.serial.read(sampleQuantity * 2)

    sampledData = [self._convert2IntDispatch(value) for value in sampledDataRaw]

    angleDiff = self._calcAngleDiff(startAngle, endAngle)

    results, checkSum = self._calcDistance(startAngle, angleDiff, F_SA, sampledData, sampleQuantity, checkSum)

    checkSumTemp = packageType
    checkSumTemp += (sampleQuantity << 8)
    checkSum ^= (checkSumTemp)
    checkSum ^= L_SA
    if checkSum == CC:
      return results
    return results

  # def _calcAngle(self, FL_SA) -> Union[int, float]:
  #   fl_sa = self._byte2Int(FL_SA)
  #   angle = (fl_sa >> 1) / 64
  #   return fl_sa, angle
  
  def _calcAngle(self, L, M) -> Union[int, float]:
    fl_sa = L
    fl_sa = fl_sa + (M << 8)
    angle = (fl_sa >> 1) // 64
    return fl_sa, angle
  
  def _calcAngleDiff(self, startAngle, endAngle):
    angleDiff = endAngle - startAngle
    if angleDiff < 0:
      angleDiff += 360
    return angleDiff
  
  def _calcDistance(self, startAngle, angleDiff, FSA, sampledDataRaw, sampledCount, checkSum):
    results = list()
    for i in range(0, sampledCount * 2, 2):
      SIL, SIM = sampledDataRaw[i], sampledDataRaw[i + 1]
      SILM = SIL
      SILM = SILM + (SIM << 8)
      checkSum ^= SILM

      distance = float(SILM) / 4

      # Get angle and correct value from distance
      angle = startAngle + (angleDiff / float(sampledCount)) * i / 2
      angleCorrection = 0
      if distance > 0:
        angleCorrection = (atan(21.8 * ((155.3 - distance) / (155.3 * distance))) * (180 / pi))
      angle += angleCorrection
      if angle > 360:
        angle -= 360

      results.append(LidarMeasure(angle, distance))
    return results, checkSum
