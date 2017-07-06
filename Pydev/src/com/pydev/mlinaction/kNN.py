'''
Created on 2017年7月5日

@author: xusheng
'''

# from numpy import array, tile
from numpy import tile, array, zeros, shape
from matplotlib import pyplot
import operator
from os import listdir
    
def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(X, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(X, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
        sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]

def file2matrix(filename):
    love_dictionary = {'largeDoses':3, 'smallDoses':2, 'didntLike':1}
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)            #get the number of lines in the file
    returnMat = zeros((numberOfLines, 3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    index = 0
    #1:flight; 2:game 3:icecream
    for line in arrayOfLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
#         print('line[%s] = %s' % (index, returnMat[index,:]))
        if(listFromLine[-1].isdigit()):
            classLabelVector.append(int(listFromLine[-1]))
        else:
            classLabelVector.append(love_dictionary.get(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

# 归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))   #element wise divide
    return normDataSet, ranges, minVals

def showimg():
    datingDataMat, datingLabels = file2matrix('d:/tmp/datingDataSet.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)

    lMat = array(datingLabels)
    s = array('b')
    s.fromlist((15 * lMat).tolist())
    
    c = array('b')
    c.fromlist((15 * lMat).tolist())
    
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    
    ax.scatter(normMat[:, 0], normMat[:, 1], s=s, c=c)
    pyplot.show()

def datingClassTest():
    hoRatio = 0.10      #hold out 10%
    datingDataMat, datingLabels = file2matrix('d:/tmp/datingDataSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print('the classifier came back with: %d, the real answer is: %d' % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print('the total error rate is: %f' % (errorCount / float(numTestVecs)))
    print(errorCount)

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix('datingDataSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream, ])
    classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print('You will probably like this person: %s' % resultList[classifierResult - 1])

def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect

def test_img2vertor():
    ret = img2vector('d:/tmp/trainingDigits/0_0.txt')
    l = ret[0].tolist()
    n_rows = range(32)
    col = 32
    for i in n_rows:
#         print(''.join(map(float2str, l[col*i:col*(i+1)-1])))
        print(''.join(map(lambda x:str(int(x)), l[col*i:col*(i+1)-1])))

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('d:/tmp/trainingDigits')           #load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('d:/tmp/trainingDigits/%s' % fileNameStr)
    
    testFileList = listdir('d:/tmp/testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('d:/tmp/testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        if i % 50 == 0 or i == (mTest - 1):
            print('classifier is dealing with files [%0.2f%%]' % ((i+1)*100/mTest))
        if (classifierResult != classNumStr):
            print('%s came back with: %d, the real answer is: %d' % (fileNameStr, classifierResult, classNumStr))
            errorCount += 1.0
    print('the total number of errors is: %d' % errorCount)
    print('the total error rate is: %f' % (errorCount / float(mTest)))


if __name__ == '__main__':
#     group, labels = createDataSet()
#     ret = classify0([0, 0.4], group, labels, 3)
#     showimg()
#     datingClassTest()
#     classifyPerson()
#     test_img2vertor()
    handwritingClassTest()