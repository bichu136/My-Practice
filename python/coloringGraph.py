class node():
    def __init__(self):
        self.color = 0
        self.neightbors = []
    def add_neightbor(self,node):
        if node not in self.neightbors:
            self.neightbors.append(node)
    def self_color(self):
        c = 0
        b = False
        while b == False:
            c+=1
            b = True
            for neightbor in self.neightbors:

                if neightbor.color == c:
                    b = False
                    break
            if b:
                self.color = c

class color():
    def __init__(self):
        self.x = 0
def coloring(node):
    stack = [node]
    while stack:
        c = stack.pop()
        if c.color == 0:
            c.self_color()
            stack = c.neightbors + stack
        else:
            break

b = [int(x) for x in input().split(' ')]
n_vectors = b[1]
n_points = b[0]
points = []
for i in range(n_points):
    points.append(node())
for i in range(n_vectors):
    b = [int(x) for x in input().split(' ')]
    x1 = b[0]
    x2 = b[1]
    points[x1].add_neightbor(points[x2])
    points[x2].add_neightbor(points[x1])
coloring(points[0])
for point in points:
    print(point.color)
