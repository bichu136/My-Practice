class knight:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def get_posible_step(self,matrix):
        posible_steps = [[-1,2], [1,2], [2,1], [2,-1], [1,-2], [-1,-2], [-2, -1], [-2, 1]]
        r = []
        i = 0
        # for i in posible_steps:
        while posible_steps:
            i = posible_steps.pop()
            _x = self.x+i[0] 
            _y = self.y+i[1]
            if _x>=len(matrix) or _x<=0:
                continue
            if _y>=len(matrix[0]) or _y<=0:
                continue
            if matrix[_x][_y]==0:
                r.append([_x,_y])
        return r
    def update_location(self,x,y):
        self.x=x
        self.y=y


# knight-tour.py
w,h = [int(i) for i in input().split()]
matrix = [[0 for j in range(w+1)] for i in range(h+1)]
begin = input()
begin = [ord(begin[0]) - ord('a')+1,int(begin[1:])]
k = knight(begin[0],begin[1])
A = w*h
stack = []
stack.append([k.x,k.y])
path = []
c=0
while stack:
    now_x,now_y = stack.pop()
    k.update_location(now_x,now_y)
    #if in backtrack
    if matrix[k.x][k.y]==1:
        matrix[k.x][k.y]=0
        path.pop()
        c-=1
        continue
    #continue the road
    c+=1
    path.append([k.x,k.y])
    matrix[k.x][k.y]=1
    posible_steps = k.get_posible_step(matrix)
    stack +=[[k.x,k.y]]+posible_steps
    if c==A:
        break
for i in path:
    print(chr(i[0]+ord('a')-1)+str(i[1]),end=" ")