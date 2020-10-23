import sys
import cProfile, pstats, io
from pstats import SortKey
import numpy
class node():
    def __init__(self):
        self.left=None
        self.right=None
        self.data=None


# arr = sys.stdin.readlines()
# a = []
# i = 0
# while i<len(arr):
#     a.append(int(arr[i]))
#     i+=1
def create_perfect_binary_tree(sorted_list):
    mid = (len(sorted_list)-1)//2
    if len(sorted_list)<=0:
        return
    if mid==0:
        print(sorted_list[0])
        if (len(sorted_list)-1)%2==1:
            create_perfect_binary_tree(sorted_list[mid+1:])
        return
    create_perfect_binary_tree(sorted_list[0:mid])
    create_perfect_binary_tree(sorted_list[mid+1:])
    root.data=sorted_list[mid]
    print(sorted_list[mid])
root = node()
i = 0
base = 10000
while i<100:
    n = base+i*base
    arr = numpy.random.randint(-1000000,1000000,size=n)
    arr = sorted(arr)
    pr = cProfile.Profile()
    pr.enable()
    cProfile.run("create_perfect_binary_tree(arr)")
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    
    break
    i+=1