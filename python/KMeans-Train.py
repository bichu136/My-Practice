import cv2 as cv
import numpy as np
import sys
import random
import time
import threading
import concurrent.futures as mirai
import concurrent as ishoni

k = 64
means = None
img_arr=None
sema = threading.Semaphore(1)

def CaculateNewMeans(clusterArray, index):
    global means, k
    for pixel in clusterArray:
        for j in range(3):
            means[index][j] += pixel[j]
    if len(clusterArray) > 0:
        for j in range(3):
            means[index][j] = means[index][j] / len(clusterArray)


def UpdateMeans(clusterArray):
    global k, means
    CalThreads = [threading.Thread(target=CaculateNewMeans, args=(clusterArray[i], i,)) for i in range(k)]

    for i in range(k):
        CalThreads[i].start()
    for i in range(k):
        CalThreads[i].join()


def EuclideanDistance(x, y):
    s = 0
    for i in range(3):
        s += (x[i] - y[i]) * (x[i] - y[i])
    return s


def Classify(pixel):
    global means
    # Classify item to the mean with minimum distance
    minimum = sys.maxsize;
    index = -1;

    for i in range(64):
        # Find distance from item to mean
        dis = EuclideanDistance(pixel, means[i]);

        if (dis < minimum):
            minimum = dis;
            index = i;

    return index;


def CalculateMeans(img_arr, maxIterations=100):
    global means, k
    belongsTo = [0 for i in range(len(img_arr))];
    # Calculate means
    for e in range(maxIterations):
        start = time.time()
        print("iteration {} times".format(e))
        # If no change of cluster occurs, halt
        clusterArray = [[] for i in range(len(means))];
        noChange = 0;
        for i in range(len(img_arr)):
            pixel = img_arr[i];
            # Classify item into a cluster and update the
            # corresponding means.
            index = Classify(pixel);
            clusterArray[index].append(pixel);

            # Item changed cluster
            if (index != belongsTo[i]):
                noChange += 1;

            belongsTo[i] = index;
        UpdateMeans(clusterArray);
        print("diff = {}".format(noChange / len(img_arr) * 100))
        if (noChange / len(img_arr) * 100 <= 1):
            break;
        print(time.time() - start)

# def CalculateMeans(maxIterations=100):
#     global means, k
#     belongsTo = [0 for i in range(len(img_arr))];
#     semaList = [threading.BoundedSemaphore]
#     # Calculate means
#     img_t = img_arr
#     count_pixel_in_groups = [0 for i in range(k)]
#     def Classify_model(index):
#         #process img_t[index] to somethings
#         for i in range(len(img_t[index])):
#             group = Classify(img_t[i],means)
#             if belongsTo[i] != group:
#                 count_pixel_in_groups[group][index]+=1
#         #TODO: add to cluster
#
#     def ChangingPercent():
#         for i in range(len(old_count)):
#             if old_count>count_pixel_in_groups:
#                 old_count[i] -= count_pixel_in_groups[i]
#             else:
#                 old_count[i] += count_pixel_in_groups[i]
#         r = 0
#         for i in range(len(old_count)):
#             r+=old_count[i]
#         return r
#     for e in range(maxIterations):
#         start = time.time()
#         print("iteration {} times".format(e))
#         # If no change of cluster occurs, halt
#         old_count = count_pixel_in_groups
#         count_pixel_in_groups_process = [[0 for i in range(k)] for j in range(8)]
#         clusterArray = [[] for i in range(k)];
#         noChange = 0;
#         img_t = img_arr
#         img_t.reshape((8,100000//8,3))
#         100000 // 8
#         CalThreads = [threading.Thread(target=Classify_model, args=(i,)) for i in range(8)]
#         for i in range(8):
#             CalThreads[i].start()
#         for i in range(8):
#             CalThreads[i].join()
#         for i in range(len(belongsTo)):
#             clusterArray[belongsTo[i]].append(img_arr[i])
#         for i in range(len(count_pixel_in_groups)):
#             count_pixel_in_groups[i] = 0
#             for j in range(8):
#                 count_pixel_in_groups[i]+=count_pixel_in_groups_process[i][j]
#
#
#         #last step
#         UpdateMeans(clusterArray);
#         changedPercent = ChangingPercent()
#         print("diff = {}".format(changedPercent))
#         if (changedPercent<=0.01):
#             break;
#         print(time.time() - start)

def InitializeMeans():
    global means,k
    # Initialize means to random number between the max and means
    # The means and max of each pixel
    number_of_channel = 3
    means = [[0 for x in range(number_of_channel)] for i in range(k)]
    for mean in means:
        for j in range(number_of_channel):
            mean[j] = random.uniform(0, 255)
    return means
def CreatePixels():
  pixel_arr = []
  for i in range(256):
    for j in range(256):
      for y in range(256):
        pixel_arr.append([i,j,y])

  return np.array(pixel_arr,dtype=np.uint8)


img_arr = CreatePixels()
means = InitializeMeans()
np.random.shuffle(img_arr)

echo = 10
for i in range(echo):
  start = time.time()
  print("learning {}\{} times".format(i,echo))
  np.random.shuffle(img_arr)
  trainning_data = img_arr[0:100000]
  CalculateMeans(trainning_data)
  end=time.time()
  print(end-start)
file = open("log.txt",mode="w+")
file.write("means:\n")
for i in range(len(means)):
  s = ""
  for channel in means[i]:
    s += str(channel)+","
  file.write(s+"\n")
file.close()
