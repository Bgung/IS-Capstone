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
      measureList = self._calcMeasure(measureList)
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
    while not found and not self.stopThread:
      # 모든 Bytes는 0xaa가 앞에 나오고 뒤에 값이 나옴 (Little endian)
      PH_1 = self.serial.read(1)
      print(PH_1)
      while (PH_1) == b'\xaa':
        pass
      PH_2 = self.serial.read(1)
      if PH_2 == b'\x55':
        # \xaa\x55 가 나오면 데이터 한 줄의 시작을 의미
        found = True
    PH = int.from_bytes(PH_1)
    PH += int.from_bytes(PH_2) << 8

    if self.stopThread:
      return list()
    
    CT = self._readByte()
    LS = self._readByte()
    CTLS = CT + (LS << 8)
    
    sampledData = list()
    sampledData.extend([PH, CTLS])
    for _ in range(0, 80, 2):
      temp = self._readByte()
      temp += (self._readByte() << 8)
      sampledData.append(temp)
    return sampledData
  
  def _calcMeasure(self, dataRaw):
    checkSum = dataRaw[0] ^ dataRaw[2]
    checkSum ^= dataRaw[1]
    checkSum ^= dataRaw[3]

    FSA = (dataRaw[2] >> 1) // 64
    LSA = (dataRaw[3] >> 1) // 64

    if FSA > LSA:
      angleDiff = abs(FSA - (360 + LSA))
    else:
      angleDiff = abs(FSA - LSA)
    
    LSN = dataRaw[1] >> 8

    sampledData = dataRaw[5: ]
    angle = [FSA]

    for i in range(1, LSN - 1):
      angle.append((angleDiff / (LSN - 1) * i) + FSA)
    angle.append(LSA)

    distance = list()
    # LSN = 40
    print(len(sampledData))
    for dist in range(LSN):
      distance.append(sampledData[dist] // 4)
    
    angleCorrected = list()

    for cor in range(LSN):
      if distance[cor] == 0:
        angleCorrected = 0
        angle[cor] = 0
      else:
        angleCorrected = math.degrees(math.atan(21.8 * (155.3 - distance[cor]) / (155.3 * distance[cor])))
        angle[cor] = abs(angle[cor] - angleCorrected)
      
      if angle[cor] >= 360:
        angle[cor] = angle[cor] - 360
      else:
        angle[cor] = angle[cor]
    
    for an, dist in zip(angle, distance):
      self.measureList.append(LidarMeasure(an, dist))
    return self.measureList

  def _calcAngle(self, FL_SA) -> Union[int, float]:
    angle = (FL_SA >> 1) / 64
    return FL_SA, angle
  
  # def _calcAngle(self, L, M) -> Union[int, float]:
  #   fl_sa = L + M * 256
  #   angle = (fl_sa >> 1) / 64
  #   return fl_sa, angle
  
  def _calcAngleDiff(self, startAngle, endAngle):
    angleDiff = endAngle - startAngle
    if angleDiff < 0:
      angleDiff += 360
    return angleDiff
  
  def _calcDistance(self, startAngle, angleDiff, FSA, sampledDataRaw, sampledCount, checkSum):
    results = list()
    for i in range(0, sampledCount * 2, 2):
      SIL, SIM = sampledDataRaw[i], sampledDataRaw[i + 1]
      checkSum ^= (SIL + SIM * 256)
      distance = float(SIL + SIM * 256) / 4
      # Get angle and correct value from distance
      angle = ((FSA + angleDiff) / float(sampledCount)) * i
      angleCorrection = 0
      if distance > 0:
        # angleCorrection = math.atan2(21.8 * (155.3 - distance), 155.3 * distance) * (180 / math.pi)
        angleCorrection = atan((21.8 * (155.3 - distance)) / (155.3 * distance)) * (180 / math.pi)
      angle += angleCorrection
      if angle > 360:
        angle -= 360

      results.append(LidarMeasure(angle, distance))
    return results, checkSum
