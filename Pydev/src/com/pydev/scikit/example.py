'''
Created on 2017年6月29日

@author: xusheng
'''

from sklearn import datasets, svm
import pickle

if __name__ == '__main__':
#     iris = datasets.load_iris()
    digits = datasets.load_digits()

    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(digits.data[:-1], digits.target[:-1])
    clf.predict(digits.data[-1:])
    
    