import sys
input = sys.argv[1]
#create a Dictionary
f = open("syllables.txt",encoding='UTF-8')
MyDict= dict()
t = f.readline().strip()
while(t!=""):
    MyDict[t] = False
    t = f.readline().strip()
r=0
k =0
f.close()
#open file and split words
f = open(input,encoding='UTF-8')
t = f.read()
words = [x.upper() for x in t.split()]
print(len(words))
#check if a word is in a Dictionary or not
for word in words:
    if word in MyDict.keys():
        #MyDict.update({word:True})
        MyDict[word] = True
#count the number of word appear in Dictionary
for val in MyDict.values():
    if val:
        r+=1
result = ((r/len(MyDict.values()))*100)
print(result)
f.close()