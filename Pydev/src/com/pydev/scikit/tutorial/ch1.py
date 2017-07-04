'''
Created on 2017年6月29日

@author: xusheng
'''

from sklearn import datasets, svm, random_projection
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelBinarizer, MultiLabelBinarizer
import numpy
import pickle
from matplotlib import pyplot

def iris_job():
    clf = svm.SVC()
    iris = datasets.load_iris()
    X, y = iris.data, iris.target
    print(X)
    print(X.shape)
    print()
    print(y)
    clf.fit(X, y)
    print(clf)
    
    s = pickle.dumps(clf)
    clf2 = pickle.loads(s)
    print(clf2.predict(X))

def digit_job():
    digits = datasets.load_digits()
    print(digits.data)
    print(digits.images.shape)
    pyplot.imshow(digits.images[-1])
    print()
    print(digits.target)
    clf = svm.SVC(gamma=0.001, C=100.)
    print(clf)
    
    clf.fit(digits.data[:-1], digits.target[:-1])
    print(clf.predict(digits.data[-1:]))
    
    

def type_casting():
    rng = numpy.random.RandomState(0)
    X = rng.rand(10, 2000)
    print(X)
    X = numpy.array(X, dtype='float32')
    print(X)
    print(X.dtype)
    
    transformer = random_projection.GaussianRandomProjection()
    X_new = transformer.fit_transform(X)
    print(X_new)
    print(X_new.dtype)

def refitting():
    rng = numpy.random.RandomState(0)
    X = rng.rand(100, 10)
    y = rng.binomial(1, 0.5, 100)
    print(X)
    print(y)
    
    X_test = rng.rand(5, 10)
    print(X_test)
    
    clf = svm.SVC()
    
    print('linear:')
    clf.set_params(kernel='linear')
    clf.fit(X, y)
    print(clf.predict(X_test))
    
    print('rbf:')
    clf.set_params(kernel='rbf')
    clf.fit(X, y)
    print(clf.predict(X_test))
    
def multi_job():
    X = [[1, 2], [2, 4], [4, 5], [3, 2], [3, 1]]
    y = [0, 0, 1, 1, 2]
    
    classif = OneVsRestClassifier(estimator=svm.SVC(random_state=0))
    classif.fit(X, y)
    
    print(classif.predict(X))
    
#     X_test = [[3, 3], [6, 7]]
#     print(classif.predict(X_test))

    y = LabelBinarizer().fit_transform(y)
    print(y)
    classif.fit(X, y)
    print(classif.predict(X))
    
    y = [[0, 1], [0, 2], [1, 3], [0, 2, 3], [2, 4]]
    y = MultiLabelBinarizer().fit_transform(y)
    print(y)
    
if __name__ == '__main__':
#     iris_job()
    digit_job()
#     type_casting()
#     refitting()
#     multi_job()
