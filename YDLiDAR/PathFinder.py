import pandas as pd
import numpy as np

from YDLidarX2 import LidarX2
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


### 라이다 학습하기 ######
#### 입력값 ########
df = pd.read_excel('C:/Users/user/Documents/4-1캡스톤/results.xlsx')
dataset = df.values
print(dataset.shape)
X = dataset.reshape((59,360,2))
print(X.shape)

######### 출력값  #######
y = np.array(['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'R',
              'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'F',
              'F', 'F', 'F', 'L', 'L', 'L', 'L', 'F', 'F', 'F',
              'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F',
              'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F',
              'R', 'R', 'R', 'R', 'R', 'R', 'R', 'F', 'F'])

# LabelEncoder를 사용하여 클래스를 숫자로 변환
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)   # 0 :F 1:L 2:R
# OneHotEncoder를 사용하여 원-핫 인코딩
onehot_encoder = OneHotEncoder(sparse=False, categories=[range(3)])
y_encoded = label_encoder.fit_transform(y.reshape(-1, 1))
onehot_encoded_labels = onehot_encoder.fit_transform(y_encoded.reshape(-1, 1))
# 데이터셋 분할
X_train, X_test, y_train, y_test = train_test_split(X, onehot_encoded_labels, test_size=0.2, random_state=42)


#########  knn 모델 #######
X_train_2d = X_train.reshape(X_train.shape[0], -1)
# Handle NaN values with SimpleImputer
imputer = SimpleImputer(strategy='mean')
X_train_2d = imputer.fit_transform(X_train_2d)
# Create and train the KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train_2d, y_train)
# 테스트 데이터에 대한 예측
X_test_2d = X_test.reshape(X_test.shape[0], -1)
y_pred = knn.predict(X_test_2d)
# 정확도 계산
accuracy = accuracy_score(y_test, y_pred)
print('Test Accuracy:', accuracy)



Lidar = LidarX2()  # 객체 만들고
with Lidar as lidar:  # with문으로 열어서 사용 => 자동으로 스캔 시작.
  # with문을 벗어나면 자동으로 Serial 연결 끊어지고, Scan Thread 종료함
  vector = np.zeros((360, 2))
  previous_vector = np.zeros((360, 2))
  vectors = []

  while True:
    result = lidar.getPolarResults()  # 극좌표계 결과 받아오기

    for angle in range(360):
      angle_str = str(angle)
      if angle_str in result:
        vector[angle, 0] = angle
        vector[angle, 1] = result[angle_str]


      if not np.array_equal(vector, previous_vector):   # 백터의 값이 변할 때마다 print
        previous_vector = vector.copy()
        # 새로운 데이터 읽기
        new_data = pd.DataFrame(vector, columns=['Angle', 'Range'])  # (360,2)
        new_data = new_data.values  # 데이터를 NumPy 배열로 변환
        # 입력 데이터 전처리
        new_data = new_data.reshape(1, 360, 2)  # 입력 데이터의 형태에 맞게 변경
        X_new_2d = new_data.reshape(new_data.shape[0], -1)

        imputer = SimpleImputer(strategy='mean')
        X_new_2d = imputer.fit_transform(X_new_2d)

        # 예측 수행
        predictions = knn.predict(X_new_2d)
        print(predictions)