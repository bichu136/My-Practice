import unicodedata
import tkinter as tk
from tkinter import filedialog
import re
import sys
import time
class Trienode():
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.children = dict()
        self.goals = None
        self.isword=False
    def insert(self,key):
        self.children[key] = Trienode(key,0)
    def query(self):
        r = self.value
        for child in self.children:
            r +=child.query()
        return r
    def search(self,str,index = 0):
        if (index == len(str)):
            self.value+=1
            return True
        c = str[index]
        if c in self.children.keys():
            i =index +1
            return self.children[c].search(str,i)
        else:
            return False
        pass
    def query(self):
        r =0
        if self.value>0 and self.isword:
            r +=1
        for child in self.children.values():
            r+= child.query()
        return r



#--------------------------------------------------#

root =Trienode('',0)

def intoTrie(str,root):
    current = root
    com = str.split()
    goal = com[0]
    concepts=com[1:]

    for c in range(0,len(concepts)):
        if concepts[c] not in current.children.keys():
            current.insert(concepts[c])
            current = current.children[concepts[c]]
        else:
            current = current.children[concepts[c]]
    current.goals = goal

source = "rule.txt"
f =  open(source, encoding='utf-8')
t = f. readline().strip()
arr = []
while(t!=''):
    intoTrie(t,root)
    t = f.readline().strip()
f.close()
windows = tk.Tk()
windows.withdraw()
target = filedialog.askopenfilename(title="Select file", filetypes=(("Text file", "*.txt"), ("All files", "*.*")))
f = open(target, encoding='utf-8-sig')


stk = []
inp = f.readline().split()
cur = inp[0]


def chooseStep(stk, cur, root):
    i=0
    j=0
    root_cur = root
    stk_cur = stk[-1]
    if stk_cur in root_cur.children.keys():
        root_cur = root_cur.children[stk_cur]
        if cur in root_cur.children.keys():
            return "shift",None,i,j
    for i in range(len(stk)):
        root_cur = root
        stk_cur = stk[i]
        j = i
        while(j<len(stk)) and (stk[j] in root_cur.children.keys()):
            root_cur=root_cur.children[stk[j]]
            j+=1
        # if root_cur.children:
        #     pass
        # else:
        #     if root_cur.goals is not None:
        #         return "Reduce",root_cur.goals,i,j
        #     continue
        # checking grammar in
        if (j>=len(stk)-1):
            if stk_cur in root_cur.children.keys():
               return "shift",None,i,j
            else:
                if root_cur.goals is not None:
                    return "Reduce",root_cur.goals,i,j
    return "shift",None,i,j




while(1):
    print("stk:{}\ncur:{}\ninp:{}\nstep:".format(stk,cur,inp),end="")
    if(stk==[]):
        stk.append(inp.pop(0))
        cur = inp[0]
        print("shift")
        continue
    name,goal,re_start,re_end = chooseStep(stk,cur,root)
    if goal is not None:
        print("{} {}".format(name, stk[re_start:re_end]))
        re_end-=1
        while(re_start<re_end):
            stk.pop(re_end)
            re_end-=1
        stk[re_start]=goal
    else:
        if cur is None:
            break
        else:
            stk.append(inp.pop(0))
        if(inp!=[]):
            cur = inp[0]
        else:
            cur=None
        print("shift")
