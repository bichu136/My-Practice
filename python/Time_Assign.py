buffer = [x for x in input().split(' ')]
n = int(buffer[0])
m = int(buffer[1])
jobs =[int(x) for x in input().split(' ')]
machines_total_time = [0] * m
jobs.sort(reverse = True) # jobs = sorted(jobs)
M_mins = 0
time_min = 0
for i in range(0,n):
    machines_total_time[M_mins]+=jobs[i]
    time_min+=jobs[i]
    for j in range(0,m):
        if machines_total_time[j]<time_min:
            time_min = machines_total_time[j]
            M_mins = j
print(machines_total_time)
