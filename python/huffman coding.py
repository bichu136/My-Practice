import sys

class TreeNode():
    def __init__(self,letter,R = None,L = None,weight = -1):
        self.letter = letter
        self.right = R
        self.left = L
        self.weight = weight
    def LNR(self):
        s = ""
        if self.left is not None:
            s +=self.left.LNR()
        if self.letter is not None:
            s+="({} {}) ".format(self.weight,self.letter)
        else:
            s += "({} {}) ".format(self.weight,"None")
        if self.right is not None:
            s+=self.right.LNR()
        return s
    def __str__(self):
        return "({},{})".format(self.letter,self.weight)
    def __repr__(self):
        return "({},{})".format(self.letter,self.weight)
    def search(self,s,p =""):
        if self is None:
            return p
        if self.left is not None:
            r =  self.left.search(s,p = p+"0")
            if r is not None:
                return r
        if self.right is not None:
            r = self.right.search(s,p = p+"1")
            if r is not None:
                return r
        if self.letter is not None:
            if self.letter == s:
                return p
def Encode(string,root):
    s = ""
    for char in string:
        s+= root.search(s = char)
    return s
def Decode(code,root):
    s = ""
    c = root
    while code !="":
        if c.letter is None:
            if code[0] == "0":
                c = c.left
                code = code[1:]
            else:
                c = c.right
                code = code[1:]
        else:
            s+=c.letter
            c = root
    if c != root:
        if c.letter is not None:
            s+=c.letter
    return s
#file = open(sys.argv[1],mode = "r")
queue = []
#iStream = file.read()
iStream ="Asuna is the best"
#file.close()
a = dict()
for char in iStream:
    if char in a.keys():
        a[char]+=1
    else:
        a[char] = 1
for key in a.keys():
    queue.append(TreeNode(key,weight = a[key]))
queue.sort(key = lambda x : x.weight)

while(len(queue)>1):
    l = queue[0]
    r = queue[1]
    w = l.weight + r.weight
    p = TreeNode(None,r,l,weight = w)
    queue.remove(l)
    queue.remove(r)
    queue.append(p)
    queue.sort(key = lambda x: x.weight)

huffman_Tree = queue[0]
code = Encode(iStream,huffman_Tree)
string = Decode(code,huffman_Tree)
print ("Huffman Tree LNR:",huffman_Tree.LNR())
print("Huffman code:",code)
print("Decode the code:",string)
