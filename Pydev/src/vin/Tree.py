'''
Created on 2017年7月10日

@author: xusheng
'''

from math import log
import operator

def splitVinFeatures(s):
    vinFeatures = []
    vinFeatures.append(s[0:3])    # WMI
    vinFeatures.append(s[3:9])    # VDS
    vinFeatures.append(s[9])  # year
    vinFeatures.append(s[10]) # assembler
#     print(vinFeatures)
    return vinFeatures

def splitLineCol(line):
    dataset = line.split(',')
    return dataset

# def createDataSet(filename):
#     dataSet = []
#     with open(filename, 'r', encoding='utf-8') as fr:
#         for line in fr.readlines():
#             record = splitLineCol(line.strip())
#             nFeatures = splitVinFeatures(record[3])
#             nFeatures.append(record[1])
#             dataSet.append(nFeatures)
#             print(nFeatures)
# 
# #     col_labels = ['id', 'model_id', 'model_name', 'vin', 'del_flag', 'asset_id']
# #     vin_labels = ['WMI', 'VDS', 'year', 'assembler']
#     return dataSet, vin_labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            # skip featVec[axis]
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # the last column is used for the labels
    baseEntropy = calcShannonEnt(dataSet)
#     print('dataSet %s \'s baseEntropy = [%s]' % (dataSet, baseEntropy))
    bestInfoGain = 0.0;
#     bestFeature = -1
    bestFeature = 0
    for i in range(numFeatures):  # iterate over all the features
        featList = [example[i] for example in dataSet]  # create a list of all the examples of this feature
        uniqueVals = set(featList)  # get a set of unique values
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
#             print('feature_column[%d], unique_value[%s], subEntropy = [%s]' % (i, value, newEntropy))
        infoGain = baseEntropy - newEntropy  # calculate the info gain; ie reduction in entropy, infoGain:BIGGER IS BETTER; newEntropy: SMALLER IS BETTER, MEANS MORE STEADY
        if (infoGain > bestInfoGain):  # compare this to the best gain so far
            bestInfoGain = infoGain  # if better than current best, set to best
            bestFeature = i
    return bestFeature  # returns an integer

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
#     print(classList)
    if classList.count(classList[0]) == len(classList): 
        return classList[0]  # stop splitting when all of the classes are equal
    if len(dataSet[0]) == 1:  # stop splitting when there are no more features in dataSet
        return majorityCnt(classList)
#     print('createTree-dataSet: ', dataSet)
    bestFeat = chooseBestFeatureToSplit(dataSet)
#     print('createTree-bestFeat: ', bestFeat)
    
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
#     print(labels)
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
#     print(uniqueVals)
    for value in uniqueVals:
        subLabels = labels[:]  # copy all of labels, so trees don't mess up existing labels
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):
    for item in inputTree.items():
        firstStr = item[0]
        break
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else:
        classLabel = valueOfFeat
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()
    
def grabTree(filename):
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

if __name__ == '__main__':
    sourcefilename = 'd:/tmp/result_training_100000.txt'
    dumpfilename = 'd:/tmp/vintree_100000.pickle'
    
#     dataSet, labels = createDataSet(sourcefilename)
#     print('dataset done!')

#     tree = createTree(dataSet, labels)
#     print('tree done!')
#     
#     storeTree(tree, dumpfilename)
#     print('all done!')
