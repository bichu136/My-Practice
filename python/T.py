import cv2 as cv
import numpy as np
import sys
import math
from random import shuffle,uniform

means = np.array([[216.23966446974237, 91.03175554224086, 227.7920910724985],
 [223.42111050027486, 220.80868609125892, 89.72457394172622],
 [30.38513101767215, 223.2699573430835, 34.5496648385131],
 [28.559673832468494, 157.76797627872497, 26.366197183098592],
 [155.37559241706163, 101.06516587677726, 67.0835308056872],
 [175.252027448534, 168.86899563318778, 86.9288833437305],
 [80.87039877300613, 28.74846625766871, 135.92177914110428],
 [220.29529780564263, 223.47021943573668, 27.044514106583073],
 [32.63256113256113, 87.47554697554698, 222.94916344916345],
 [31.690824468085108, 30.6156914893617, 92.91422872340425],
 [213.104469273743, 91.15530726256983, 28.45195530726257],
 [226.7709090909091, 163.10424242424241, 134.0939393939394],
 [146.3706896551724, 26.646551724137932, 159.2493842364532],
 [222.9636923076923, 27.96, 220.21046153846154],
 [102.93556701030928, 96.32023195876289, 229.3943298969072],
 [92.328079392878, 28.970227670753065, 219.28312901342673],
 [25.35623749166111, 100.49566377585057, 154.35156771180786],
 [37.1578947368421, 94.65233506300963, 24.61749444032617],
 [171.5242165242165, 27.378205128205128, 92.11324786324786],
 [153.80520199225236, 222.4803541781959, 220.92584394023243],
 [27.950064020486554, 216.41165172855312, 226.6190781049936],
 [26.852298417483045, 32.465712132629996, 30.863602110022608],
 [108.88869153345175, 165.24629958555357, 106.42155121373594],
 [94.16421568627452, 170.35049019607843, 224.41973039215685],
 [221.03320802005013, 29.44360902255639, 157.4624060150376],
 [27.45811320754717, 30.23245283018868, 161.1290566037736],
 [220.4963421496905, 224.27180641530668, 161.93078221722004],
 [157.87600246761258, 186.18075262183837, 170.19000616903145],
 [91.35641547861508, 217.22606924643586, 24.808553971486763],
 [221.62929358392742, 29.093324692158134, 31.145171743357096],
 [88.80196078431372, 228.0660130718954, 218.75228758169933],
 [227.37672465506898, 95.9742051589682, 164.79244151169766],
 [97.93365794278759, 223.1290322580645, 81.16859403530128],
 [120.22964509394572, 87.36186499652052, 120.18719554627697],
 [156.02611464968152, 33.30828025477707, 28.06433121019108],
 [225.57490396927017, 111.18822023047375, 88.38028169014085],
 [225.6070601851852, 157.90972222222223, 35.810763888888886],
 [223.82686414708886, 157.86721144024514, 213.69509703779366],
 [32.68802588996764, 225.57022653721683, 102.24724919093852],
 [118.83870967741936, 91.60906298003073, 22.09984639016897],
 [166.55139550714773, 131.7569775357386, 144.91490810074882],
 [220.42761319172723, 221.5953046394634, 225.1587479038569],
 [85.97079169869332, 29.318985395849346, 26.531898539584933],
 [99.29972299168975, 220.67146814404433, 152.20997229916898],
 [186.2574942352037, 73.17755572636433, 122.34050730207532],
 [30.358078602620086, 28.826783114992722, 224.1688500727802],
 [33.46175438596491, 228.20070175438596, 164.73754385964912],
 [33.71701846965699, 165.1325857519789, 85.39050131926122],
 [110.71661721068249, 28.4013353115727, 81.7826409495549],
 [230.6814569536424, 36.9523178807947, 91.02185430463577],
 [155.56043329532497, 224.14196123147093, 38.149372862029644],
 [160.41931464174453, 226.9956386292835, 118.37133956386293],
 [91.00233372228705, 150.49591598599767, 39.165110851808635],
 [161.55031627372054, 142.68027602070154, 225.52501437607822],
 [97.91908585546634, 141.17356392835083, 171.23162445954293],
 [154.88223552894212, 84.08383233532935, 189.09913506320692],
 [23.942263279445726, 96.20169361046959, 84.11547344110855],
 [66.20115416323166, 120.4080791426216, 112.159109645507],
 [32.724256292906176, 148.29290617848972, 220.37986270022884],
 [82.02869139258223, 75.38208537438769, 172.43456962911128],
 [33.86292654713707, 167.61711972238288, 155.25853094274146],
 [156.0105003088326, 155.5787523162446, 25.551575046324892],
 [158.92852664576802, 34.66457680250784, 227.51912225705328],
 [79.95474452554744, 79.80875912408759, 69.92408759124088]])






def MinAndMaxOfAllPixel(img_arr):
    n = img_arr.shape[1]
    vMax = [sys.maxsize]*img_arr.shape[1]
    vMin = [-sys.maxsize-1]*img_arr.shape[1]
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
    return s

def InitializeMeans(k,cMin,cMax,img_arr):
    #Initialize means to random number between the max and means
    #The means and max of each pixel
    print(img_arr)
    number_of_channel = len(img_arr[0])
    means = [[0]*number_of_channel]*k
    for mean in means:
        for i in range(number_of_channel):
            mean[i] = int(uniform(cMin[i]+1,cMax[i]-1))
    return means
def updateMean(n,mean,pixel):
    for i in range(pixel):
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
    clusters = [[]*k]
    for pixel in img_arr:
        index = Classify(means,pixel)
        clusters[index].append(item)
    return clusters


def CalculateMeans(k, img_arr, maxIterations=100000):
    # Find the minima and maxima for columns
    cMin, cMax = MinAndMaxOfAllPixel(img_arr);

    # Initialize means at random points
    means = InitializeMeans(k, cMin, cMax,img_arr);

    # Initialize clusters, the array to hold
    # the number of items in a class
    clusterSizes = [0]* k;

    # An array to hold the cluster an item is in
    belongsTo = [0]* len(img_arr);

    # Calculate means
    for e in range(maxIterations):
        # If no change of cluster occurs, halt
        noChange = True;
        for i in range(len(img_arr)):
            pixel = img_arr[i];
            # Classify item into a cluster and update the
            # corresponding means.

            index = Classify(means, pixel);

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

def compress_img(img,means):
    w = img.shape[0]
    h = img.shape[1]
    img = img.reshape((w * h,3))
    compress = []
    for pixel in img:
        compress.append(Classify(means,pixel))
    compress = np.array(compress,dtype = np.uint8)
    return compress.reshape(w,h)
def decompress_img(img,means):
    w = img.shape[0]
    h = img.shape[1]
    img = img.reshape((w*h))
    decompress = []
    for pixel in img:
        decompress.append(means[pixel])
    decompress = np.array(decompress,dtype = np.uint8)
    return np.reshape(decompress,(w,h,3))
def main():
    img = cv.imread("test4.jpg")
    img = cv.resize(img,(550,550))
    img_compress = compress_img(img,means)
    img_decompress = decompress_img(img_compress,means)
    cv.imwrite('1.png',img_decompress)
    cv.imshow('img',img_decompress)
    cv.waitKey(0)
    cv.destroyAllWindows()
main()
