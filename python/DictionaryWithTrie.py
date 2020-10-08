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
    for c in range(0,len(str)):
        if str[c] not in current.children.keys():
            current.insert(str[c])
            current = current.children[str[c]]
        else:
            current = current.children[str[c]]
        if(c == (len(str)-1)):
            current.isword=True

source = "syllables.txt"
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
full = f.read()
full = full.upper()
target_name = f.name.split("/")[-1]
words = (re.split('\W+', full))
t = time.time()
c = 0
for word in words:
    if (root.search(word)):
        c+=1
counter = root.query()
percentage = counter*100/7746
end = time.time()
print("time cost:",end-t)
print("Có", counter, "tiếng trong danh sách file", source, "xuất hiện trong file", target_name)
print("Tỷ lệ phần trăm xuất hiện là:", percentage)
