def Min(arr):
    n = len(arr)
    min = arr[0]
    mini = 0
    for i in range(n):
        if arr[i]<min:
            min = arr[i]
            mini = i
    return min,mini
buffer = [x for x in input().split(' ')]
n = int(buffer[0])
m = int(buffer[1])
jobs = []
for i in range(0,m):
    buffer = [int(x) for x in input().split(' ')]
    jobs.append([])
    for index,value in enumerate(buffer):
        jobs[i].append((index,value))
time_of_machines = [0]*m
for machine in jobs:
    machine.sort(key = lambda tup : tup[1])

while(n>0):
    min = time_of_machines[0]
    equal_to_min = []
    for i in range(0,m):
        if time_of_machines[i]<min:
            min = time_of_machines[i]
            equal_to_min = [i]
        elif time_of_machines[i] == min:
            equal_to_min.append(i)
    print(equal_to_min[0])
    print(jobs[equal_to_min[0]][0])
    min = jobs[equal_to_min[0]][0][1]
    l = len(equal_to_min)
    machine_to_do = equal_to_min[0]
    for i in range(0,l):
        if min < jobs[equal_to_min[i]][0][1]:
            min = jobs[i][0][1]
            machine_to_do = equal_to_min[i]
    time_of_machines[machine_to_do] += min
    # delete jobs have been done
    index_of_job = jobs[machine_to_do][0][0]
    for i in range(0,m):
        for j in range(0,n):
            if jobs[i][j][0] == index_of_job:
                del jobs[i][j]
                break

    n-=1
print(time_of_machines)
