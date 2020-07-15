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
import pyaudio
import pydub.playback
# set global variable
CHUNK = 1024
# open file
file_path = "/home/bichu136/Downloads/audio.mp3"
audio_segment = pydub.AudioSegment.from_mp3(file_path)

# create interface to PortAudio
port_interface = pyaudio.PyAudio()
# # Open a .Stream object to write the WAV file to
# # 'output = True' indicates that the sound will be played rather than recorded
stream = port_interface.open(format = port_interface.get_format_from_width(audio_segment.sample_width),
                channels = audio_segment.channels,
                rate = audio_segment.frame_rate,
                output = True)
                # stream_callback=callback)
# # stream.start_stream()
# i=0
# data = audio_segment.get_frame(i)
# i+=1
# while data != '':
#     stream.write(data)
#     data = audio_segment.get_frame(i)
#     i+=1
# stream.stop_stream()
# stream.close()
# port_interface.terminate()

y = np.array(audio_segment.get_array_of_samples())
if audio_segment.channels==2:
    y = y.reshape((-1,2))
frame_rate = audio_segment.frame_rate
data = y
data = np.rot90(data)
print(data.shape)
print(frame_rate)
left = np.array(data[0])
right = np.array(data[1])


fig, ax = plt.subplots(1, figsize=(15, 7))
ax.set_title('spectrum')
ax.set_xlabel('freq')
ax.set_ylabel('amplitude')
ax.set_xbound(25,1000)
ax.set_ylim(5000000)

line, =ax.plot(np.zeros((1024,)))
# plt.setp(ax)
plt.show(block=False)
print(audio_segment.frame_count(180000))
i=0
data = audio_segment.get_frame(i)
i+=1
while data != '':
    stream.write(data)
    data = audio_segment.get_frame(i)
    if i%1024==0:
        ax.set_xbound(25, 1000)
        a = np.abs(np.fft.fft(left[i-1024:i]))
        line.set_ydata(a)
        fig.canvas.draw()
        fig.canvas.flush_events()
    i+=1
# i=0
# data = audio_segment.get_frame(i)
# i+=1
# while data != '':
#     stream.write(data)
#     data = audio_segment.get_frame(i)
#     i+=1
# stream.stop_stream()
# stream.close()
# port_interface.terminate()

# stream.close()
# port_interface.terminate()