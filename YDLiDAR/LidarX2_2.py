# 센서에서 데이터 읽어서 데이터 파싱해서 각도, 거리 계산
import serial
import sys
import math
import numpy as np
import cv2


class YdlidarX2:

    def __init__(self, port):
        self.port = port

    # 센서와 연결 시도 : 시리얼 통신 연결 설정
    def Connect(self):
        try:
            self.ydlidarX2 = serial.Serial(self.port,
                                           115200,
                                           bytesize=serial.EIGHTBITS,
                                           parity=serial.PARITY_NONE,
                                           stopbits=serial.STOPBITS_ONE,
                                           timeout=None)

            self.scan_code = bytes([0xA5, 0x5A, 0x05, 0x00, 0x40, 0x81])
            self.ydlidarX2.write(self.scan_code)

            # self.ydlidarX2.close()


        except Exception as e:
            self.ydlidarX2.close()
            print(e)
            sys.exit()

    # 센서에서 데이터 읽어들임 : raw_data 에 데이터 저장
    def GetSerial(self):

        while True:
            # self.ydlidarX2.open()
            # 한번에 보내는 패킷 크기 : 90byte
            raw_data = bytearray(self.ydlidarX2.read(90))
            # self.ydlidarX2.close()

            #
            ph_temp = raw_data[0]
            ph_temp += raw_data[1] << 8
            ctls_temp = raw_data[2]
            ctls_temp += raw_data[3] << 8

            if ph_temp == 0x55AA and ctls_temp == 0x2800:
                i = 0
                self.data = []
                while i < 90:
                    temp = raw_data[i]
                    temp += raw_data[i + 1] << 8
                    self.data.append(temp)
                    i += 2
                break
            else:
                continue

    # 각도, 거리값 계산 : GetSerial 함수에서 읽어온 데이터를 처리
    # 첫번째 4바이트 데이터 = 체크섬 계산
    # 5번째 데이터부터 distance , angle 배열 생성
    # 각 샘플의 거리 정보 이용한 각도보정(angle_correct) 계산
    # 각도보정 값 이용해 측정된 각도 정보 보정(angle)
    def Calculate(self):
        check_sum = self.data[0] ^ self.data[2]
        check_sum ^= self.data[1]
        check_sum ^= self.data[3]

        an_fsa = (self.data[2] >> 1) // 64
        an_lsa = (self.data[3] >> 1) // 64

        if an_fsa > an_lsa:
            ang_diff = abs(an_fsa - (360 + an_lsa))
        else:
            ang_diff = abs(an_fsa - an_lsa)

        lsn = self.data[1] >> 8

        sampled_data = self.data[5:]
        angle = [an_fsa]

        i = 0

        for i in range(1, lsn - 1):
            angle.append((ang_diff / (lsn - 1) * i) + an_fsa)

        angle.append(an_lsa)

        distance = []

        for dist in range(lsn):
            distance.append(sampled_data[dist] // 4)

        ang_correct = []

        for cor in range(lsn):
            if distance[cor] == 0:
                ang_correct = 0
                angle[cor] = 0
            else:
                ang_correct = math.degrees(math.atan(21.8 * (155.3 - distance[cor]) / (155.3 * distance[cor])))
                angle[cor] = abs(angle[cor] - ang_correct)

            if angle[cor] >= 360:
                angle[cor] = angle[cor] - 360
            else:
                angle[cor] = angle[cor]
        return angle, distance


ydlidarX2 = YdlidarX2('COM3')
ydlidarX2.Connect()

img = np.zeros((512, 512, 3), np.uint8)

while True:
    ydlidarX2.GetSerial()
    angle, distance = ydlidarX2.Calculate()
    print('angle : {0}, distance : {1}'.format(angle, distance))
    print(len(angle))

    for i in range(len(distance)):
        # opencv 그림이 viewer랑 비슷
        x = (distance[i]) / 15 * math.cos(math.radians(angle[i]))
        y = (distance[i]) / 15 * math.sin(math.radians(angle[i]))
        cv2.circle(img, (256 + int(x), 256 + int(y)), 1, (255, 255, 255), -1)

        # print로 나오는 angle-distance 값 viewer랑 비슷
        centerX, centerY = 256, 256  # 이미지 중심 좌표 설정
        x = int(distance[i] * math.cos(math.radians(angle[i])))
        y = int(distance[i] * math.sin(math.radians(angle[i])))
        cv2.circle(img, (x + centerX, y + centerY), 2, (255, 255, 255), -1)  #  x와 y 좌표가 이미지에서 중앙을 기준으로 한 좌표계에서 좌우 대칭적으로 배치
        cv2.imshow('', img)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    if k == 27:
        break

cv2.destroyAllWindows()