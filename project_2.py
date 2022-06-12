import time
import numpy as np
import copy
import matplotlib.pyplot as plt

def distanceSquare(data1,data2,fetures):
    """
    calculate the square of the distance
    :param data1: row1
    :param data2: row2
    :param fetures: column of the feature set we chose
    :return: square of the distance
    """
    sumD = 0
    for f in fetures:
        x = data1[f] - data2[f]
        sumD += x * x
    return sumD

def accuracy(data,fetures):
    """
    this function is the traditional way to calculate the accuracy,
    just use the loop to compare every rows, this way is very slow.
    :param data: numpy matrix
    :param fetures: list, the features subset
    :return: float, accuracy
    """
    correctly = 0
    for i in range(len(data)):
        nnDistance = float('inf')
        nnLable = 0

        # compare with the orthers rows to find the nearst neighbor
        for j in range(len(data)):
            if i == j:
                continue

            # I just use the square, it will not influence the result, I hope this can save time.
            currDistance = distanceSquare(data[i],data[j],fetures)
            if currDistance < nnDistance:
                nnDistance = currDistance
                nnLable = data[j][0]
        if data[i][0] == nnLable:
            correctly += 1
    return correctly/len(data)

def accuracy2(data,fetures):
    """
    This function is very very fast, it use the broadcast feature of the numpy,
    it use the matrix to calculate the all the distance and then the second smallest is
    the nearest neighbor,(the smallest one is itself, so we choose the second)
    :param data: numpy matrix
    :param fetures: list, the fetures subset
    :return: float, accuracy
    """
    correctly = 0
    currData = data[:,fetures] #take the coloum we need
    for i in range(len(data)):
        currRow = currData[i]
        currRow = currRow.reshape(1, -1) #reshap the currrow to 2 dimension
        dist = np.sum(np.square(currData - currRow), axis=1)
        dist = np.sqrt(dist)
        nnLoaction = np.argsort(dist)[1]
        if data[i][0] == data[nnLoaction][0]:
            correctly += 1
    return correctly/len(data)

if __name__ == '__main__':

    # get the data file path
    print('please input the file path:')
    path = input()

    # choose the algorithm, 1 is forward, 2 is backward
    print('1 is forward, 2 is backward:')
    algorithm = int(input())
    # calculate the running time
    start = time.time()
    path = '/home/xgao058/cs205_data/s34.txt'
    data = np.loadtxt(path)
    data01 = data
    featureNumbers = len(data[0])-1
    # I use the set to store the features because the search speed is fast than list
    currFeatures = set()
    result = []
    maxK = 0 # the max accuracy

    # forward select
    if algorithm == 1:

        for i in range(1,featureNumbers+1):
            k = 0 # the max accuracy of current depth
            maxAccuracyF = 0
            for j in range(1,featureNumbers+1):
                # wether the current seleted feature was already in the set
                if j in currFeatures:
                    continue
                temp = copy.copy(currFeatures)
                temp.add(j)
                currK = accuracy2(data,list(temp)) # the accuracy of current node
                print('    Features set',temp, '; accuracy: %5.1f' % (currK*100), '%')
                if currK > k:
                    k = currK
                    maxAccuracyF = j
            # choose the best feature set and update current set
            currFeatures.add(maxAccuracyF)
            # store final best feature set
            if k > maxK:
                maxK = k
                bestFeatures = copy.copy(currFeatures)
            print('Best set:', currFeatures, '; accuracy: %5.1f' % (k * 100), '%')
            result.append([list(currFeatures), k])
        end1 = time.time()
        print('**Finished** The best features subset:',bestFeatures ,'; accuracy: %5.1f' % (maxK*100),'%')
        print('forward runtime:','%8.3f s' %(end1-start))

    # backward eliminate
    else:
        result2 = []
        # initial features set
        for i in range(1,featureNumbers+1):
            currFeatures.add(i)
        maxK = accuracy2(data,list(currFeatures))
        print('Best set:', currFeatures, '; accuracy: %5.1f' % (maxK * 100), '%')

        for i in range(1, featureNumbers ):
            if algorithm == 1:
                break
            k = 0  # accuracy
            maxAccuracyF = 0
            # remain =
            for j in range(1, featureNumbers + 1):
                if j not in currFeatures:
                    continue
                temp = copy.copy(currFeatures)
                temp.remove(j)
                currK = accuracy2(data, list(temp))
                if currK > k:
                    k = currK
                    maxAccuracyF = j
                print('    Features set',temp, '; accuracy: %5.1f' % (currK * 100),'%')
            currFeatures.remove(maxAccuracyF)
            if k > maxK:
                maxK = k
                bestFeatures = copy.copy(currFeatures)
            print('Best set:',currFeatures , '; accuracy: %5.1f' % (k * 100), '%')
            result.append([list(currFeatures),k])
        end2 = time.time()
        print('**Finished** The best features subset:', bestFeatures, '; accuracy: %5.1f ' % (maxK*100),'%')
        print('backward runtime:', '%8.3f s'%( end2- start))
