import sys
out = open("out.txt","w")
sys.stdout = out
def sum_of_all_chosen_ele(list1,number_of_ele_1,list2,number_of_ele_2):
    sum=0
    if number_of_ele_1!=0:
        i =number_of_ele_1 
        while(i>0):
            i-=1
            sum+=list1[i]
    if number_of_ele_2!=0:
        i =number_of_ele_2
        while(i>0):
            i-=1
            sum+=list2[i]
    return sum
tc = int(input())
while tc>0:
    n,m,k = [int(i) for i in input().split()]
    list1 = [int(i) for i in input().split()]
    list2 = [int(i) for i in input().split()]
    k+=1
    if m<=k: 
        number_of_ele_2 =m 
    else: 
        number_of_ele_2 =k
    number_of_ele_1 = k-number_of_ele_2
    sum = sum_of_all_chosen_ele(list1,number_of_ele_1,list2,number_of_ele_2)
    number_of_ele_1_f=number_of_ele_1
    number_of_ele_2_f=number_of_ele_2
    min_sum = sum
    while(number_of_ele_1<k and number_of_ele_1<n and number_of_ele_2>=0):
        number_of_ele_1+=1
        number_of_ele_2-=1
        sum = sum - list2[number_of_ele_2]+list1[number_of_ele_1-1]
        if min_sum>sum:
            min_sum = sum
            number_of_ele_1_f=number_of_ele_1
            number_of_ele_2_f=number_of_ele_2
        else: 
            break
    if number_of_ele_1_f==0:
        print(list2[number_of_ele_2_f-1])
    elif number_of_ele_2_f==0:
        print(list1[number_of_ele_1_f-1])
    else:
        if list1[number_of_ele_1_f-1]>list2[number_of_ele_2_f-1]:
            print(list1[number_of_ele_1_f-1])
        else:
            print(list2[number_of_ele_2_f-1])
    tc-=1