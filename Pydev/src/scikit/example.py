'''
Created on 2017年6月29日

@author: xusheng
'''

import numpy as np

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
from sklearn.preprocessing import MultiLabelBinarizer

def example():
    arr = np.random.rand(4, 4)
    ma = np.mat(arr)
    inv_ma = ma.I
    print('array =\n', arr)
    print('matrix =\n', ma)
    print('inv_matrix =\n', inv_ma)
    print('matrix * inv_matrix =\n', ma * inv_ma)
    print('matrix * inv_matrix - eye(4) =\n', ma * inv_ma - np.eye(4))

def binarizeFeatures():
    testdata = pd.DataFrame({'pet': ['cat', 'dog', 'dog', 'fish'], 'age': [4, 6, 3, 3], 'salary': [4, 5, 1, 1]})
#     print(testdata.age)
#     petVec = OneHotEncoder(sparse = False).fit_transform(testdata.pet.values.reshape(-1, 1))
    petVec = LabelBinarizer().fit_transform(testdata.pet.values)
    ageVec = OneHotEncoder(sparse = False).fit_transform(testdata.age.values.reshape(-1, 1))
    salVec = OneHotEncoder(sparse = False).fit_transform(testdata.salary.values.reshape(-1, 1))
    finVec = np.hstack((ageVec, salVec))
#     finVec = OneHotEncoder(sparse = False).fit_transform(testdata[['age', 'salary']].values)
    print(finVec)

if __name__ == '__main__':
    binarizeFeatures()
    
