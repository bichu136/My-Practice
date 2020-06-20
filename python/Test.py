# import threading
# import time
# import numpy
# semList = [threading.Semaphore(0) for i in range(4)]
# def x(index):
#     a = numpy.random.randint(1, 100)
#     a = a / 50
#     time.sleep(a)
#     if index ==0:
#         pass
#     else:
#         semList[index].acquire()
#
#     print(index)
#     if index ==3:
#         pass
#     else:
#         semList[index + 1].release()
#
# threads = [threading.Thread(target=x,args=(i,)) for i in range(4)]
#
# for i in range(4):
#     threads[i].start()
# for i in range(4):
#     threads[i].join()
# start = time.time()
# a=0
# def EuclideanDistance(x, y):
#     s = 0
#     for i in range(3):
#         s += (x[i] - y[i]) * (x[i] - y[i])
#     return s
# start = time.time()
# for i in range(10000):
#     for i in range(64):
#         EuclideanDistance([236.4322315,297.16169147,196.96197],[196.5211651,254.26816,181.9176123])
# print(time.time()-start)

import cv2 as cv
import numpy as np
import csv, time, random, math, sys
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pycuda.driver as drv


mod = SourceModule("""
      __global__ void classify_model(int * data,int * w,int * means,int *out)
      {
        int idx = blockIdx.x;
        int idy = blockIdx.y;
        int locate = (idy+idx*w[0]);
        long min =9999999999;
        int li=-1;
        int i;
        long k;
        int j;
        long sum;
        for(i=0;i<64;i++)
        {
            sum = 0;
            k=0;
            for(j=0;j<3;j++)
            {
                k = means[i*3+j]-data[locate*3+j];
                sum=sum+ (k*k);
            }
            if (sum<min)
            {
                min=sum;
                li=i;
            }
        }
        out[locate]=li;
      }
      __global__ void update_means_model(int * cluster_arrays,int*cluster_len,float*means)
      {
        int cluster_index = blockIdx.x;
        int color_channel=blockIdx.y;
        long offset = 0;
        long i;
        for(i=0;i<cluster_index;i++)
        {
            offset+=cluster_len[i];
        }
        //cluster_arrays[offset]=0;
        long locate = offset*3+color_channel;
        //int r = means[cluster_index*3+color_channel];
    //    for(i=0;i<cluster_len[cluster_index];i++)
    //    {
    //        cluster_arrays[locate+i*3]=0    ;
    //    }
    //    cluster_arrays[locate]=offset;
        //means[cluster_index*3+color_channel] = r/(cluster_len[cluster_index]+i);
      }
      """)


classify_model = mod.get_function("classify_model")
update_means_model = mod.get_function("update_means_model")

img = cv.imread("3.jpg")
print(img.dtype)
np_img = np.array(img,dtype=np.int32)
means = np.array([[92, 78, 220],
 [26, 215, 172],
 [41, 228, 227],
 [35, 229, 119],
 [227, 215, 88],
 [30, 102, 226],
 [228, 138, 104],
 [173, 102, 90],
 [90, 182, 32],
 [106, 22, 98],
 [173, 227, 36],
 [162, 222, 175],
 [32, 170, 105],
 [126, 80, 98],
 [164, 106, 221],
 [228, 211, 27],
 [95, 139, 224],
 [74, 77, 82],
 [105, 148, 87],
 [89, 172, 166],
 [93, 230, 165],
 [30, 218, 22],
 [26, 139, 167],
 [159, 159, 142],
 [36, 170, 225],
 [227, 77, 94],
 [86, 37, 157],
 [35, 85, 25],
 [117, 222, 228],
 [227, 89, 224],
 [225, 228, 155],
 [213, 225, 225],
 [223, 168, 157],
 [29, 30, 217],
 [226, 22, 74],
 [43, 225, 67],
 [127, 107, 161],
 [222, 130, 31],
 [30, 71, 165],
 [156, 166, 25],
 [165, 226, 107],
 [222, 159, 222],
 [153, 39, 167],
 [172, 32, 35],
 [110, 231, 34],
 [220, 28, 219],
 [225, 54, 24],
 [106, 214, 103],
 [30, 26, 119],
 [69, 28, 36],
 [171, 31, 108],
 [93, 22, 220],
 [118, 37, 29],
 [156, 36, 228],
 [212, 99, 163],
 [84, 121, 28],
 [178, 166, 76],
 [23, 97, 92],
 [224, 31, 152],
 [27, 150, 38],
 [146, 99, 29],
 [70, 116, 134],
 [154, 171, 220],
 [21, 29, 42]],dtype=np.int32)
print(means.shape)
print(np_img.shape)
w = [np_img.shape[1]]
h = [np_img.shape[0]]
number_of_collumn = np.array(w,dtype=np.int32)
out = np.zeros((h[0],w[0]),dtype=np.int32)
start_time = time.time()
classify_model(cuda.InOut(np_img),cuda.InOut(number_of_collumn),cuda.InOut(means),cuda.InOut(out),block=(1,1,1),grid = (h[0],w[0]))
_out = out.tolist()
cluster_arrays=[[] for i in range((len(means)))]
start = time.time()
for i in range(len(_out)):
    for j in range(len(_out[i])):
        cluster_arrays[out[i][j]].append(img[i][j].tolist())
print(time.time()-start)
cluster_len = np.array([len(cluster_arrays[i]) for i in range(len(means))],dtype=np.int32)
cluster_arrays = np.array(cluster_arrays)
print(cluster_len.dtype)
print(cluster_arrays.shape)
# print(cluster_arrays)
#update_means_model(int * cluster_arrays,int*cluster_len,float*means)
update_means_model(cuda.InOut(cluster_arrays),cuda.InOut(cluster_len),cuda.InOut(means),block=(1,1,1),grid=(len(cluster_arrays),3))
for i in range(len(cluster_arrays)):
    if len(cluster_arrays[i])>0:
    print(cluster_arrays[i][0])
print(time.time()-start_time)
cv.imwrite("2_com.jpg",img_out)

#
# import cv2 as cv
# import numpy as np
# import csv, time, random, math, sys
# import pycuda.driver as cuda
# import pycuda.autoinit
# from pycuda.compiler import SourceModule
# import pycuda.driver as drv
#
#
# mod = SourceModule("""
#       __global__ void blockInfo(int * data)
#       {
#         int idx = blockIdx.x;
#         int idy = blockIdx.y;
#         data[idy+idx*4000] = 1;
#       }
#       """)
#
#
# blockInfo = mod.get_function("blockInfo")
#
# zero = np.zeros((4001,4000),dtype = np.int32)
#
# print(zero)
# zero_in_gpu = cuda.mem_alloc(zero.size*zero.dtype.itemsize)
# cuda.memcpy_htod(zero_in_gpu,zero)
# blockInfo(zero_in_gpu,block=(1,1,1),grid = (4001,4000))
# pc = np.empty_like(zero)
# cuda.memcpy_dtoh(pc,zero_in_gpu)
# print(pc)
