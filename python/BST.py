class TreeNode():
    def __init__(self,right = None,left = None,weight = -1):
        self.right = right
        self.left = left
        self.weight = weight
    def __str__(self):
        return "({})".format(self.weight)
    def __repr__(self):
        return "({})".format(self.weight)

i = 0
arr = []
t = input()
while (t!="3"):
    k = t.split()
    if k[0]=="0":
        arr.append(int(k[1]))
    if k[0]==="1":
        arr.insert(0,int(k[1]))
    if k[0]=="2":
        i = 0
        a = int(k[1])
        b = int(k[2])
        while i<len(arr):
            if arr[i]==a:
                break
             i+=1
        if i+1>len(arr):
            arr.insert(0,b)
        else:
            arr.insert(i+1,b)
    t = input()
inp = arr[i]
i+=1
r=None
while(inp!=0):
    n = TreeNode(weight=inp)
    c = r
    p = None
    k = False
    if r == None:
        r=n
    else:
        while c!=None:
            if n.weight>c.weight:
                p = c
                c = c.right
            elif n.weight<c.weight:
                p = c
                c = c.left
            else:
                k = True
                break
        if k:
            inp=int(input())
            continue
        if n.weight>p.weight:
            p.right = n
        elif n.weight<p.weight:
            p.left = n
    inp=arr[i]
    i+=1
def count_Leaf(current):
    if current==None:
        return 0
    # print(current.right,current.left,current)
    c_r = count_Leaf(current.right)
    c_l = count_Leaf(current.left)
    if c_r+c_l==0:
        return 1
    else:
        return c_r+c_l
def height(current):
    if current==None:
        return 0
    # print(current.right,current.left,current)
    c_r = height(current.right)
    c_l = height(current.left)
    if c_r>c_l:
        return c_r+1
    else:
        return c_l+1
print(height(r))
