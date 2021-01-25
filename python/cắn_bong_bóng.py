# import random as rand
a = int(input())
begin = []
for i in range(a):
  begin.append(int(input()))



# stack = [{"step":begin,"total":0}]
# _max = 0
# def get_next_state(state):
#   list_of_state=[]
#   if len(state["step"])==0:
#       return []
#   if len(state["step"])==1:
#       return [{"step":[],
#                  "total":state["total"]+state["step"][0]}]
#   for i in range(len(state["step"])):
#     if i==0:
#       total = state["step"][i]*state["step"][i+1]
#     elif i==len(state["step"])-1:
#       total = state["step"][i]*sta
#       te["step"][i-1]
#     else:
#       total = state["step"][i+1]*state["step"][i]*state["step"][i-1]
#     new_state = {"step":[state["step"][j] for j in range(len(state["step"])) if j != i],
#                  "total":state["total"]+total}
#     list_of_state.append(new_state)
#   return list_of_state


# while stack:
#     current = stack.pop()
#     if _max< current["total"]:
#         _max = current["total"]
#     stack = stack+ get_next_state(current)
# print(_max)
def calc(i,a):
    if len(a)==1:
        x = a[i]
    elif i==len(a)-1:
        x= a[i]*a[i-1]
    elif i==0:
        x= a[i]*a[i-1]
    else: x =  a[i]*a[i-1]*a[i+1]
    a.pop(i)
    return x
def d_c(arr):
    max_ = 0
    if len(arr)==0:
        return 0
    for i in range(len(a)):
        tmp = [i for i in arr]
        max_ = max(max_,d_c(tmp[:i])+d_c(tmp[i+1:])+calc(i,a)))
    return max_