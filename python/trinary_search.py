def trinary_search(sorted_list,find_ele,count=1):
    # print(sorted_list,find_ele)
    n= len(sorted_list)-1
    m1=n//3
    m2=m1+n//3+1
    if n==0:
        return -1,count
    if sorted_list[m1]==find_ele:
        return m1,count
    if sorted_list[m2]==find_ele:
        return m2,count
    if m1==m2:
        return -1,count
    if find_ele<sorted_list[m1]:
        # print(m1,sorted_list[m1],m2,sorted_list[m2],find_ele)
        res,t_c=trinary_search(sorted_list[0:m1],find_ele,count+1)
        if res ==-1:
            return res,t_c
        return res,t_c
    if find_ele>sorted_list[m2]:
        res,t_c=trinary_search(sorted_list[m2:],find_ele,count+1)
        if res ==-1:
            return res,t_c
        return res+m2,t_c
    res,t_c=trinary_search(sorted_list[m1:m2],find_ele,count+1)
    if res ==-1:
            return res,t_c
    return res+m1,t_c
input()
k = [int(i) for i in input().split()]
input()
test=[int(i) for i in input().split()]

for i in test:
    print(trinary_search(k,i))
    print("-----------------")
