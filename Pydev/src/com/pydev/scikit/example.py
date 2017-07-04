'''
Created on 2017年6月29日

@author: xusheng
'''

from sklearn import datasets, svm, random_projection
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer, OneHotEncoder
import numpy
import pickle
import pandas

def example():
    testdata = pandas.DataFrame({
'pet': ['cat', 'dog', 'dog', 'fish'],                         
'age': [4 , 6, 3, 3],                         
'salary':[4, 5, 1, 1]
})
    print(testdata)
    
    encoder = OneHotEncoder(sparse = False)
#     obj1 = encoder.fit_transform(testdata['pet'].values.reshape(-1, 1))
    obj2 = encoder.fit_transform(testdata['age'].values.reshape(-1, 1))
    obj3 = encoder.fit_transform(testdata['salary'].values.reshape(-1, 1))
    X = numpy.hstack((obj2, obj3))
    print(X)
    print(encoder.feature_indices_)

if __name__ == '__main__':
    example()
    