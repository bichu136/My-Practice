import pyaudio as au
import scipy as sci
import pydub
import numpy as np
import scipy.io.wavfile as ostr
import matplotlib.pyplot as plt
import math
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import time


# open file
file_path = "%USER%/Desktop/audio.mp3"
normalized = False
a = pydub.AudioSegment.from_mp3(file_path)
y = np.array(a.get_array_of_samples())
if a.channels==2:
    y = y.reshape((-1,2))
if normalized:
    frame_rate =  a.frame_rate
    data =np.float32(y) / 2 ** 15
else:
    frame_rate = a.frame_rate
    data = y
data = np.rot90(data)
print(data.shape)
print(frame_rate)

left = np.array(data[0])
right = np.array(data[1])
#DFT in GPU
cuda_model = SourceModule("""
#define PI 3.14159265359
__device__ float cos_func(float phi)
{
  return cos(phi);
}
__device__ float sin_func(float phi)
{
  return sin(phi);
}
__device__ float sqrt_func(float phi)
{
  return sqrt(phi);
}
__global__ void DiscreteFourierTransform(int16_t * wave, float * wave_out,int* waveLength)
{ 
  int l = waveLength[0];
  float re=0,im=0;
  for(int i=0;i<l;i++){
    float phi = (PI *i * blockIdx.x)/l;
    re += wave[i] * cos_func(phi);
    im -= wave[i] * sin_func(phi);
  }
  float t = re*re+im*im;
  wave_out[blockIdx.x] = sqrt_func(t);
}
""")
DiscreteFourierTransform = cuda_model.get_function("DiscreteFourierTransform")

gpu_out = np.zeros(1000, dtype=np.float32)
l = np.array([left.shape[0]])
start = time.time()
arr = []
i = 0
fig, ax = plt.subplots(1, figsize=(15, 7))
ax.set_title('spectrum')
ax.set_xlabel('freq')
ax.set_ylabel('amplitude')
ax.set_xbound(25,1000)
ax.set_ylim(5000000)

line, =ax.plot(gpu_out)
# plt.setp(ax)
plt.show(block=False)

start = time.time()
while (i < 10000):
    gpu_out = np.zeros(1000, dtype=np.float32)

    start = i * 1000
    end = start + 1000
    gpu_in = np.array(left[start:end])
    l = np.array([gpu_in.shape[0]])

    DiscreteFourierTransform(cuda.InOut(gpu_in), cuda.InOut(gpu_out), cuda.In(l), block=(1, 1, 1), grid=(1000, 1))
    # print(gpu_out)
    ax.set_xbound(25, 1000)
    line.set_ydata(gpu_out)
    fig.canvas.draw()
    fig.canvas.flush_events()
    i += 1
end = time.time()
print(end - start)

