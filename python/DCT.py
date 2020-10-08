from scipy.fftpack import dctn,idctn
import numpy as np

arr = np.array([[2,5,5,2],[3,1,3,9],[2,8,0,5],[7,2,0,7]])
DCT = dctn(arr,norm='ortho')


print(DCT)