import csv, time, random, math, sys
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy
import pycuda.driver as drv
import cupy
k=64
means = []
mempool = cupy.get_default_memory_pool()
pinned_mempool = cupy.get_default_pinned_memory_pool()

#------------------create CUDA functions-----------------#
K_means = SourceModule("""
    __global__ void classify(float * means, int *trainning_data, int * belongs_to, int * data_size, int * means_size)
    {
        int idx = blockIdx.x;
        int li;
        float least = 99999999;
        for(int i = 0; i< means_size[0]; i++){
            float sum = 0.0;
            for(int j = 0; j< data_size[0]; j++){
            sum += ((means[i*data_size[0] + j] - trainning_data[idx*date_size[0] +j])* (means[i*data_size[0] + j] - trainning_data[idx*data_size[0] +j]));
            }
            if( sum < least){
                least  = sum;
                li = i;
                }
        }
        belongs_to[idx] = li;
    }
    """)

classify_model = Classify_model.get_function("classify")
def ClassifyArrayWithGPU(trainning_data):
    """
    Classify all data row to a specific means
    """
    global means,k,mempool,pinned_mempool,classify_model
    data_size =[len(trainning_data[0])]
    data_size = numpy.array(data_size,dtype = numpy.int32)

    belongs_to=[0 for i in range(len(trainning_data))]
    belongs_to=numpy.array(belongsTo,dtype = numpy.int32)

    trainning_size = [len(trainning_data)]
    trainning_size=numpy.array(trainning_size,dtype = numpy.int32)

    means_size = [k]
    means_size=numpy.array(means_size,dtype = numpy.int32)
    #bring the data to gpu
    #data need
    #   * means
    #   * trainning_data
    #   * belongsTo write again
    #   * data_size(3)
    #   * means_size(k)

    means_in_gpu = cuda.mem_alloc(k*means.dtype.itemsize)
    cuda.memcpy_htod(means_in_gpu,means)

    belongs_to_in_gpu = cuda.mem_alloc(belongs_to.size*belongs_to.dtype.itemsize)
    cuda.memcpy_htod(belongs_to_in_gpu,belongs_to)

    trainning_size_in_gpu = cuda.mem_alloc(trainning_size.dtype.itemsize)
    cuda.memcpy_htod(trainning_size_in_gpu,trainning_size)

    data_size_in_gpu = cuda.mem_alloc(data_size.dtype.itemsize)
    cuda.memcpy_htod(data_size_in_gpu,data_size)

    means_size_in_gpu =cuda.mem_alloc(means_size.dtype.itemsize)
    cuda.mem_htod(means_size_in_gpu,means_size)
    #Calculate
    classify_model(means_in_gpu,trainning_data_in_gpu,belongs_to_in_gpu,data_size_in_gpu,means_size_in_gpu)
    cuda.memcpy_dtoh(belongs_to_in_gpu,belongs_to)
    count_datas_in_means = [0 for in range(k)]
    #release gpu's ram

    return belongsTo
def ChangingPercentage(old,new):
    return percentage
    pass
def UpdateMeans(belongsTo,trainning_data):
    """
    Update the set of means
    """
    global means,k
    #brings the data to gpu

    #calculate
    return
def InitializeMeans():
    """
    we can random the set of means
    """"
    global means,k
    pass
def InitializeColor():
    """
    Initialize set of  100000 colors
    """
    pass
def CalculateMeans(trainning_data,maxIterations):
    """
    Claasify then update Means
    """
    global means,k

    for i in range(maxIterations):
        if i>0:
            old_count = count_datas_in_means
        belongsTo,count_datas_in_means = ClassifyArrayWithGPU(trainning_data)
        if i>0:
            if ChangingPercent(old_count,count_datas_in_means)<1:
                break
        UpdateMeans(belongsTo)
    pass
def main():
    """
    Real program
    """
    global means,k
    #get the trainning_data
    InitializeMeans()

    echo = 10
    for i in range(echo):
        print("learning {}/{}}".format(i+1,echo))
        trainning_data = InitializeColor()
        start = time.time()
        CalculateMeans(trainning_data)
        print(time.time()-start)
