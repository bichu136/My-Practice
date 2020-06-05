import cv2 as cv
import numpy as np
import sys
import random
import time
def MinAndMaxOfAllPixel(img_arr):
    n = img_arr.shape[1]
    vMax = [-sys.maxsize-1]*img_arr.shape[1]
    vMin = [sys.maxsize]*img_arr.shape[1]
    for pixel in img_arr:
        for index_channel in range(n):
            if vMax[index_channel] <pixel[index_channel]:
                vMax[index_channel] = pixel[index_channel]
            if vMin[index_channel] >pixel[index_channel]:
                vMin[index_channel] = pixel[index_channel]
    return vMax,vMin

def EuclideanDistance(x,y):
    s = 0
    for i in range(3):
        s+= (x[i]-y[i])*(x[i]-y[i])
    return np.sqrt(s)

def InitializeMeans(k,cMin,cMax,img_arr):
    #Initialize means to random number between the max and means
    #The means and max of each pixel
    number_of_channel = len(img_arr[0])
    means = [[0 for x in range(number_of_channel)] for i in range(k)]
    for mean in means:
        for j in range(number_of_channel):
            mean[j] = random.uniform(cMin[j],cMax[j])
    return means
def updateMean(n,mean,pixel):
    for i in range(len(pixel)):
        m = mean[i]
        m = (m * (n-1)+pixel[i])/float(n)
        mean[i] = m
    return mean


def Classify(means, pixel):
    # Classify item to the mean with minimum distance
    minimum = sys.maxsize;
    index = -1;

    for i in range(len(means)):
        # Find distance from item to mean
        dis = EuclideanDistance(pixel, means[i]);

        if (dis < minimum):
            minimum = dis;
            index = i;

    return index;

def FindCluster(means,img_arr,k):
    clusters = []
    for pixel in img_arr:
        index = Classify(means,pixel)
        clusters[index].append(pixel)
    return clusters


def CalculateMeans(k, img_arr, maxIterations=100000):
    # Find the minima and maxima for columns
    cMax, cMin = MinAndMaxOfAllPixel(img_arr);

    # Initialize means at random points
    means = InitializeMeans(k, cMin, cMax,img_arr);

    # Initialize clusters, the array to hold
    # the number of items in a class
    clusterSizes = [0 for i in range(len(means))];

    # An array to hold the cluster an item is in
    belongsTo = [0 for i in range(len(img_arr))];

    # Calculate means
    for e in range(1):
        # If no change of cluster occurs, halt
        noChange = True;
        for i in range(len(img_arr)):
            pixel = img_arr[i];
            # Classify item into a cluster and update the
            # corresponding means.
            index = Classify(means, pixel);

            clusterSizes[index] += 1;
            means[index] = updateMean(clusterSizes[index], means[index], pixel);

            # Item changed cluster
            if (index != belongsTo[i]):
                noChange = False;

            belongsTo[i] = index;

        # Nothing changed, return
        if (noChange):
            break;

    for mean in means:
        for i in range(len(mean)):
            mean[i]=int(mean[i])
    return means,clusterSizes;

def compress_img(img_arr,means):
    img_arr_compressed = []
    for i in range(len(img_arr)):
        index = Classify(means,img_arr[i])
        img_arr_compressed.append(index)
    return np.array(img_arr_compressed,dtype=np.uint8)
def decompress(img_arr_compress,means):
    output = []
    for pixel in img_arr_compress:
        output.append(means[pixel])
    return np.array(output,dtype=np.uint8)
def main():
    img = cv.imread("3.jpg")
    file = open("log.txt",mode="w+")
    cv.imshow('img',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    start = time.time()
    img_arr = np.reshape(img,(img.shape[0]*img.shape[1],img.shape[2]))
    k = 10
    means,clusterSizes = CalculateMeans(k,img_arr)
    # means = [[176, 253, 60], [231, 119, 186], [228, 43, 146], [77, 89, 150], [88, 81, 106], [250, 169, 69], [15, 210, 242], [226, 236, 247], [140, 141, 163], [169, 188, 230]]
    img_arr_compress = compress_img(img_arr,means)
    img_output_arr = decompress(img_arr_compress,means)
    img_output = img_output_arr.reshape((img.shape[0],img.shape[1],img.shape[2]))
    stop = time.time()
    print(stop-start)
    cv.imshow('img', img_output)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite("2_com.jpg",img_output)
    # log the means
    file.write("means:\n")

    for i in range(len(means)):
        s = ""
        for channel in means[i]:
            s += str(channel)+","
        file.write(s+"\n")
    #log the img_arr_compress
    file.write("img_arr_compress:\n")
    s = ""
    for i in range(len(img_arr_compress)):
        s += str(img_arr_compress[i])+" "
    file.write(s+"\n")
    file.write("clusterSizes::\n")
    s = ""
    for i in range(len(clusterSizes)):
        s += str(clusterSizes[i])+" "
    file.write(s + "\n")
    file.close()
main()
