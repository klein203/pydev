'''
Created on 2017年7月21日

@author: xusheng
'''

from sklearn import svm

def loadDataSet(fileName):
    dataMat = []
    labelMat = []
    with open(fileName) as fr:
        for line in fr.readlines():
            lineArr = line.strip().split('\t')
            dataMat.append([float(lineArr[0]), float(lineArr[1])])
            labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

if __name__ == '__main__':
    sourcefilename = 'd:/tmp/ch6/testSet.txt'
    X, y = loadDataSet(sourcefilename)
    
    clf = svm.SVC(0.6, kernel='rbf')
    clf.fit(X[:-1], y[:-1])
    print(clf)
    
#     testX = [[]]
    predict = clf.predict(X[-1])
    print('expected %s, predict %s' % (y[-1], predict))
#     clf.decision_function(testX) 
#     clf.score(testX, y)
