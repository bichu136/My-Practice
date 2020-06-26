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
     __global__ void decode_model(int *data,float*means,int*out,int *w)
     {
       int idx = blockIdx.x;
       int idy = blockIdx.y;
       int locate = (idy+idx*w[0]);
       for(int i=0;i<3;i++){
           out[locate*3+i] = means[data[locate]*3+i];
       }
     }
     __global__ void update_means_model(int * cluster_arrays,int*cluster_len,int*means)
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
    classify_model(cuda.InOut(x),cuda.InOut(number_of_collumn),cuda.InOut(np_means),cuda.InOut(out),cuda.InOut(_k),block=(1,1,1),grid = (h[0],w[0]))
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
        #update_means_model(int * cluster_arrays,int*cluster_len,float*means)
        UpdateMeans(cluster_arrays,means);
        if ChangingPercent(cluster_len_old,cluster_len<=0.001):
            break


    return means,out
def main(img_directory,out_dir,dim):
    img = cv.imread(img_directory)
    img = cv.resize(img,dim)
    # file = open("log.txt",mode="w+")
    cv.imshow('img',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    start = time.time()
    k = 64
    # means = initialize_means(k)
    # means,compressed_img = calculatte_means(means,img,k)
    # print(compressed_img.dtype)
    means = [[211.3338086442732,219.46222359717274,242.14817110765304],
             [18.899798525046652,150.7533007521689,39.30343365385091],
             [156.91312051307332,110.44829935858507,27.507783869597652],
             [54.70317817749971,225.2596579359125,207.26407237079957],
             [33.43211922769979,30.214808668763347,231.735644891399],
             [111.11668810566583,228.84975775079602,126.61021411483641],
             [109.27176851433096,180.88378241830878,100.705088977291],
             [65.78781484549455,12.866670771062033,11.068122576759588],
             [158.9993717023279,32.57486419194625,124.63303497306107],
             [231.38554310377012,172.49362104386577,32.98077787626156],
             [133.02697736137569,182.50478945844975,30.414620558323083],
             [105.79553799758072,143.8553525387231,11.571290835839653],
             [223.27095051780245,41.011832316363865,74.37135577402853],
             [215.26912975594823,58.16253090742264,21.04974442195442],
             [18.571102908930065,108.13062673492055,63.155666540025095],
             [243.8062153883592,87.28396391024567,100.40705100474766],
             [119.78873741098391,85.15990167196468,210.94341392545107],
             [235.74129886797058,17.98592519772164,125.35220173323547],
             [18.40332502309195,214.28175662361969,58.46177108859959],
             [231.00462136184655,207.21334558647004,121.18083132543657],
             [161.47951238829052,31.887832884831354,28.947761700046705],
             [176.45333945732477,239.5353204556069,69.28461658923818],
             [221.65223851523874,69.10324913870153,135.87376299882655],
             [232.45096200380996,118.28457768592487,143.84734996393337],
             [98.07763390155753,175.23085947513835,201.6655369199113],
             [143.54633979839355,67.40756074804263,75.81423764506765],
             [229.8254272602015,94.1558497985662,227.47535311008346],
             [69.5892912569805,122.72165831961951,24.953031039683967],
             [111.90969615106329,97.94036539269797,141.70614961883132],
             [49.202748982435025,167.03585323208816,159.4922073366036],
             [116.80722200004672,143.02458609562945,142.60758700992483],
             [41.991414416988924,230.67645838053016,124.27870723346149],
             [11.878673715649649,190.0796609586007,139.01068423575603],
             [202.3687320463642,126.09684602153155,78.58124963865686],
             [86.20583694401816,235.40085259065194,24.648690375569906],
             [24.723399903132208,164.65113196682242,213.25300893903733],
             [145.4802901921753,152.9048477742498,86.90746875781801],
             [103.61041261917647,239.8813950393228,221.22808132015365],
             [89.66626194271258,179.2648111750775,134.16633976966529],
             [212.63688828179747,73.7347299614423,201.27247556016192],
             [30.030644827631157,136.77111902299308,118.45072228143744],
             [58.71129310973202,95.65736926023193,150.969449796965],
             [186.15503531979164,90.80993983368793,166.34386607085838],
             [38.680775336244714,70.2951971431345,87.46067742803092],
             [59.32282207295126,186.02286626539464,56.99200251206381],
             [157.71338079835496,112.77715033777162,141.82006710723658],
             [234.35401102525594,157.90640175726978,217.7879389177531],
             [22.191458921568184,52.34333564099371,156.56265078188792],
             [66.15780499061357,13.00229660256396,68.62673113178346],
             [76.10063694416502,118.28398703889535,224.86338138231767],
             [170.74073430171032,199.726189441873,93.68919183111205],
             [221.45514009182335,228.35920546153275,200.3713432272398],
             [109.68800417267485,103.91751900949698,87.77411324387391],
             [40.38097355230722,62.85634414144444,19.761417065431928],
             [70.7514317022395,139.6345802471542,124.24629382182826],
             [143.21631210022704,160.48753812588578,237.05423755010113],
             [43.0642206396379,129.18962759333485,80.07448276431914],
             [202.9675398000245,24.06276947896113,208.45272400315156],
             [139.35573325800286,35.35252510865818,209.83921176503014],
             [99.78226139269655,37.944724240669444,57.32910543169676],
             [73.38978578701128,42.518588282927645,183.86608048422326],
             [177.83956539506636,192.03698584540587,191.75699767213266],
             [213.6333485831074,144.21752574693633,166.77289257745602],
             [20.898222771978876,21.23164681155177,64.35578069933172]]
    # means = [[176, 24, 226], [229, 164, 51], [231, 29, 43], [227, 115, 224], [25, 34, 230], [227, 174, 218], [95, 35, 164], [27, 126, 28], [43, 227, 227], [85, 22, 225], [142, 96, 157], [29, 74, 76], [29, 155, 152], [118, 162, 142], [35, 154, 88], [217, 91, 160], [163, 220, 92], [95, 209, 87], [115, 234, 218], [107, 231, 145], [149, 224, 30], [228, 230, 208], [72, 153, 226], [175, 211, 230], [130, 48, 221], [82, 230, 31], [229, 158, 141], [178, 89, 223], [148, 103, 31], [230, 36, 214], [221, 105, 27], [132, 31, 30], [29, 228, 165], [165, 31, 160], [31, 33, 174], [151, 81, 96], [119, 183, 217], [84, 29, 50], [221, 224, 33], [82, 109, 175], [227, 222, 114], [32, 225, 97], [22, 176, 221], [84, 88, 31], [26, 211, 31], [136, 128, 227], [171, 24, 89], [30, 35, 27], [224, 91, 92], [73, 190, 167], [76, 82, 227], [81, 100, 108], [116, 144, 78], [168, 164, 31], [32, 24, 109], [104, 32, 108], [179, 146, 103], [185, 44, 28], [28, 90, 140], [24, 107, 217], [175, 220, 160], [88, 164, 28], [226, 31, 131], [175, 152, 181]]
    compressed_img = compress_img(img,means,k)
    img_output = decompress(compressed_img,means,k)
    # print(img_output)
    stop = time.time()
    print(stop-start)
    # # cv.imshow('img', img_output)
    # # cv.waitKey(0)
    # # cv.destroyAllWindows()
    cv.imwrite(out_dir,img_output)



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
main("1.jpg","1com.jpg",(500,500))
main("1.jpg","1com.jpg",(1000,1000))
main("1.jpg","1com.jpg",(1500,1500))
main("1.jpg","1com.jpg",(2000,2000))
