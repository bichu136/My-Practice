import sys
import flashtext
import time
import re
#----------------THINGS FOR PARSING-------------#
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


