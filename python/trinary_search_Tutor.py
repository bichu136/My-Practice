# trinary_search_Tutor.py
def trinary_search(a,l,r,x):
    c=1
    while(r>l):
        m1 = (2*l+r)//3
        m2 = (l+2*r)//3 +1
        if a[m1 == x]: return(m1,c)
        elif x<a[m1]:
            r=m1-1
            c+=1
        elif x==a[m2]: return (m2,c)
        elif x<a[m2]:
            l=m1+1
            r=m2-1
            c+=1
        else:
            l=m2+1
            c+=1
    return -1,c
n = int(input())
arr = [int(i) for i in input().split()]
m=int(input())
arr2 = [int(i) for i in input().split()]
i=0
while(i<m):
    print(trinary_search(arr,0,n-1,arr2[i]))
    i+=1
