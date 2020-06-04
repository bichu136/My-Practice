import cv2 as cv
import numpy as np
import sys
import math
from random import shuffle,uniform
def MinAndMaxOfAllPixel(img_arr):
    n = img_arr.shape[1]
    vMax = [sys.intsize]*img_arr.shape[1]
    vMin = [-sys.intsize-1]*img_arr.shape[1]
    for pixel in img_arr:
        for index_channel in range(n):
            if vMax[index_channel] <pixel[index_channel]:
                vMax[index_channel] = pixel[index_channel]
            if vMax[index_channel] >pixel[index_channel]:
                vMax[index_channel] = pixel[index_channel]
    return vMax,vMin

def EuclideanDistance(x,y):
    s = 0
    for i in range(3):
        s+= (x[i]-y[i])**2
    return math.sqrt(s)

def InitializeMeans(k,cMin,cMax,img_arr):
    #Initialize means to random number between the max and means
    #The means and max of each pixel
    number_of_channel = len(img_arr[0])
    means = [[0]*number_of_channel]*k
    for mean in means:
        for i in range(number_of_channel):
            mean[i] = int(uniform(cMin,cMax))
    return means
def updateMean(n,mean,pixel):
    for i in range(pixel):
        m = mean[i]
        m = (m * (n-1)+pixel[i])/float(n)
        mean[i] = m
    return mean


def Classify(means, item):
    # Classify item to the mean with minimum distance
    minimum = sys.maxsize;
    index = -1;

    for i in range(len(means)):
        # Find distance from item to mean
        dis = EuclideanDistance(item, means[i]);

        if (dis < minimum):
            minimum = dis;
            index = i;

    return index;

def FindCluster(means,items,k):
    clusters = [[]*k]
    for item in items:
        index = Classify(means,items)
        clusters[index].append(item)


def CalculateMeans(k, items, maxIterations=100000):
    # Find the minima and maxima for columns
    cMin, cMax = MinAndMaxOfAllPixel(items);

    # Initialize means at random points
    means = InitializeMeans(items, k, cMin, cMax);

    # Initialize clusters, the array to hold
    # the number of items in a class
    clusterSizes = [0 for i in range(len(means))];

    # An array to hold the cluster an item is in
    belongsTo = [0 for i in range(len(items))];

    # Calculate means
    for e in range(maxIterations):
        # If no change of cluster occurs, halt
        noChange = True;
        for i in range(len(items)):
            item = items[i];
            # Classify item into a cluster and update the
            # corresponding means.

            index = Classify(means, item);

            clusterSizes[index] += 1;
            means[index] = updateMean(clusterSizes[index], means[index], item);

            # Item changed cluster
            if (index != belongsTo[i]):
                noChange = False;

            belongsTo[i] = index;

        # Nothing changed, return
        if (noChange):
            break;

    return means;

def main():
    img = cv.imread("MousePad.png")
    cv.imshow('img',img)
    cv.waitKey(0)
    img_arr = np.reshape(img,(img.shape[0]*img.shape[1],img.shape[2]))
    print(img_arr)
    cv.destroyAllWindows()

main()