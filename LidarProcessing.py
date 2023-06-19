import os

import pandas as pd

def find(FILE_NAME):
  if not FILE_NAME.endswith('.xlsx'):
    raise ValueError('File must be a .xlsx file')

  df = pd.read_excel('./files/' + FILE_NAME, names=['Angle', 'distance'])

  err_angle = list()
  for idx in range(len(df) - 1):
    angle_1, angle_2 = df.iloc[idx]['Angle'], df.iloc[idx + 1]['Angle']
    angle_1 = str(angle_1).split('.')[0]
    angle_2 = str(angle_2).split('.')[0]
    
    if angle_1 == angle_2:
      err_angle.append(angle_1)

  return err_angle

results = list()
for file in os.listdir('./files'):
  if not file.endswith('.xlsx'):
    continue
  err = find(file)
  results.append({
    'file': file,
    'errors': err
  })

results = pd.DataFrame.from_records(results)

results.to_excel('results.xlsx', index=False)