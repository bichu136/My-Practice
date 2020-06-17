import threading
import time
import numpy
semList = [threading.Semaphore() for i in range(4)]
def x(index):
    a = numpy.random.randint(1, 100)
    a = a / 50
    time.sleep(a)
    if index ==0:
        pass
    else:
        semList[index].acquire()

    print(index)
    if index ==3:
        pass
    else:
        semList[index + 1].release()

threads = [threading.Thread(target=x,args=(i,)) for i in range(4)]

for i in range(4):
    threads[i].start()
for i in range(4):
    threads[i].join()