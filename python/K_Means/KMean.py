import cv2 as cv
import numpy as np
import csv, time, random, math, sys
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pycuda.driver as drv
import threading
def CaculateNewMeans(clusterArray, index,means):
    for pixel in clusterArray:
        for j in range(3):
            means[index][j] += pixel[j]
    if len(clusterArray) > 0:
        for j in range(3):
            means[index][j] = means[index][j] / len(clusterArray)


def UpdateMeans(clusterArray,means):
    CalThreads = [threading.Thread(target=CaculateNewMeans, args=(clusterArray[i], i,means)) for i in range(len(means))]

    for i in range(len(means)):
        CalThreads[i].start()
    for i in range(len(means)):
        CalThreads[i].join()

def ChangingPercent(old_count,count_pixel_in_means):
    for i in range(len(old_count)):
        if old_count[i]>count_pixel_in_means[i]:
            old_count[i] = old_count[i] - count_pixel_in_means[i]
        else:
            old_count[i] = count_pixel_in_means[i] -old_count[i]
    r = 0
    for i in range(len(old_count)):
        r+=old_count[i]
    return r//100000*100
#------------------create CUDA functions-----------------#
cuda_model = SourceModule("""
      __global__ void classify_model(int * data,int * w,float * means,int *out,int*_k)
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
           int len=64;
           len = _k[0];

           for(i=0;i<len;i++)
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
     __global__ void decode_model(int *data,float*means,int*out,int *w,int *k)
     {
       int idx = blockIdx.x;
       int idy = blockIdx.y;
       int locate = (idy+idx*w[0]);
       for(int i=0;i<3;i++){
           out[locate*3+i] = means[data[locate]*3+i];
       }
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
       if (cluster_len[cluster_index]>0){
           long locate = offset*3+color_channel;
           float r = means[cluster_index*3+color_channel];
           for(i=0;i<cluster_len[cluster_index];i++)
           {
                r = r+cluster_arrays[locate+i*3];
           }
           r = r/cluster_len[cluster_index];

           means[cluster_index*3+color_channel] = int(r);
       }
     }
      """)
classify_model = cuda_model.get_function("classify_model")
decode_model = cuda_model.get_function("decode_model")
update_means_model = cuda_model.get_function("update_means_model")
def initialize_means(k):
    # Initialize means to random number between the max and means
    # The means and max of each pixel
    number_of_channel = 3
    means = [[0 for x in range(number_of_channel)] for i in range(k)]
    for mean in means:
        for j in range(number_of_channel):
            mean[j] = random.uniform(0, 255)
    return means
def compress_img(img,means,k):
    """
    Classify all data row to a specific means
    """
    x = np.array(img,dtype =np.int32)
    np_means = np.array(means,dtype=np.float32)
    means_size = np.array([len(means)],dtype=np.int32)
    _k=np.array([k],dtype=np.int32)
    w = [x.shape[1]]
    h = [x.shape[0]]
    number_of_collumn = np.array(w,dtype=np.int32)
    out = np.zeros((h[0],w[0]),dtype=np.int32)
    classify_model(cuda.InOut(x),cuda.InOut(number_of_collumn),cuda.InOut(np_means),cuda.InOut(out),cuda.InOut(_k),block=(1,1),grid = (h[0],w[0]))
    return out

def decompress(img_compress,means,k):
    np_means = np.array(means,dtype=np.float32)
    _k=np.array([k])
    w = [img_compress.shape[1]]
    h = [img_compress.shape[0]]
    number_of_collumn = np.array(w,dtype=np.int32)
    out = np.zeros((img_compress.shape[0],img_compress.shape[1],3),dtype=np.int32)
    #decode_model(int *data,int*means,int*out,int *w)
    decode_model(cuda.InOut(img_compress),cuda.InOut(np_means),cuda.InOut(out),cuda.InOut(number_of_collumn),cuda.InOut(_k),block=(1,1,1),grid=(h[0],w[0]))
    return out
def calculatte_means(means,img,k,max_iterations=100):
    """
    calculate new set of means
    """
    x = np.array(img,dtype =np.int32)
    np_means = np.array(means,dtype=np.float32)
    means_size = np.array([len(means)],dtype=np.int32)
    _k=np.array([k])
    w = [x.shape[1]]
    h = [x.shape[0]]
    number_of_collumn = np.array(w,dtype=np.int32)
    out = np.zeros((h[0],w[0]),dtype=np.int32)
    cluster_len = np.zeros((len(means)))
    for i in range(max_iterations):
        pass
        print("not pass")
        cluster_len_old = cluster_len
        out = np.zeros((h[0],w[0]),dtype=np.int32)
        classify_model(cuda.InOut(x),cuda.InOut(number_of_collumn),cuda.InOut(np_means),cuda.InOut(out),cuda.InOut(_k),block=(1,1,1),grid = (h[0],w[0]))
        cluster_arrays=[[] for i in range((len(means)))]
        for i in range(len(out)):
            for j in range(len(out[i])):
                cluster_arrays[out[i][j]].append(img[i][j])
        cluster_len = np.array([len(cluster_arrays[i]) for i in range(len(means))],dtype=np.int32)
        cluster_arrays = np.array(cluster_arrays)
        pc = np.zeros((np_means.shape[0],np_means.shape[1]),dtype=np.int32)
        # print(cluster_arrays)
        #update_means_model(int * cluster_arrays,int*cluster_len,float*means)
        UpdateMeans(cluster_arrays,means);
        if ChangingPercent(cluster_len_old,cluster_len<=0.001):
            break


    return means,out
def main(img_directory,imgout_directory,_k):
    img = cv.imread(img_directory)
    # img = cv.resize(img)
    # file = open("log.txt",mode="w+")
    # cv.imshow('img',img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    start = time.time()
    k = _k
    means = initialize_means(k)
    means,compressed_img = calculatte_means(means,img,k)
    start=time.time()
    c = compressed_img.tolist()
    compress_img = np.array(c,dtype=np.uint8)
    stop = time.time()
    print(stop-start)
    # print(compressed_img.dtype)
    # means = [[176, 24, 226], [229, 164, 51], [231, 29, 43], [227, 115, 224], [25, 34, 230], [227, 174, 218], [95, 35, 164], [27, 126, 28], [43, 227, 227], [85, 22, 225], [142, 96, 157], [29, 74, 76], [29, 155, 152], [118, 162, 142], [35, 154, 88], [217, 91, 160], [163, 220, 92], [95, 209, 87], [115, 234, 218], [107, 231, 145], [149, 224, 30], [228, 230, 208], [72, 153, 226], [175, 211, 230], [130, 48, 221], [82, 230, 31], [229, 158, 141], [178, 89, 223], [148, 103, 31], [230, 36, 214], [221, 105, 27], [132, 31, 30], [29, 228, 165], [165, 31, 160], [31, 33, 174], [151, 81, 96], [119, 183, 217], [84, 29, 50], [221, 224, 33], [82, 109, 175], [227, 222, 114], [32, 225, 97], [22, 176, 221], [84, 88, 31], [26, 211, 31], [136, 128, 227], [171, 24, 89], [30, 35, 27], [224, 91, 92], [73, 190, 167], [76, 82, 227], [81, 100, 108], [116, 144, 78], [168, 164, 31], [32, 24, 109], [104, 32, 108], [179, 146, 103], [185, 44, 28], [28, 90, 140], [24, 107, 217], [175, 220, 160], [88, 164, 28], [226, 31, 131], [175, 152, 181]]
    # img_compress = compress_img(img,means,k)
    img_output = decompress(compressed_img,means,k)
    # print(img_output)
    # # cv.imshow('img', img_output)
    # # cv.waitKey(0)
    # # cv.destroyAllWindows()
    cv.imwrite(imgout_directory,img_output)



    # log the means
    # file.write("means:\n")
    #
    # for i in range(len(means)):
    #     s = ""
    #     for channel in means[i]:
    #         s += str(channel)+","
    #     file.write(s+"\n")
    #log the img_arr_compress
    # file.write("img_arr_compress:\n")
    # s = ""
    # for i in range(len(img_arr_compress)):
    #     s += str(img_arr_compress[i])+" "
    # file.write(s+"\n")
    # file.write("clusterSizes::\n")
    # s = ""
    # for i in range(len(clusterSizes)):
    #     s += str(clusterSizes[i])+" "
    # file.write(s + "\n")
    # file.close()
main("1.jpg","1-16_com.jpg",16)
main("1.jpg","1-64_com.jpg",64)
main("1.jpg","1-256_com.jpg",256)
# main("2.jpg","2-16_com.jpg",16)
# main("2.jpg","2-64_com.jpg",64)
# main("2.jpg","2-256_com.jpg",256)
# main("3.jpg","3-16_com.jpg",16)
# main("3.jpg","3-64_com.jpg",64)
# main("3.jpg","3-256_com.jpg",256)
# main("5.png","5-16_com.jpg",16)
# main("5.png","5-64_com.jpg",64)
# main("5.png","5-256_com.jpg",256)
# main("1.jpg","6-16_com.jpg",16)
# main("6.jpg","6-16_com.jpg",32)
# main("6.jpg","6-64_com.jpg",64)
# main("6.jpg","6-64_com.jpg",128)
# main("6.png","6-256_com.jpg",256)
