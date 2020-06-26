import sys
import flashtext
input = sys.argv[1]

#create a Dictionary

keywordProcessor = flashtext.KeywordProcessor()
keywordProcessor.add_keyword("của","OF")
keywordProcessor.add_keyword("thuộc","OF")
keywordProcessor.add_keyword("là","BE")
keywordProcessor.add_keyword("và","AND")
keywordProcessor.add_keyword("bằng","EQUAL")
keywordProcessor.add_keyword("=","EQUAL")
f = open("keywords.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"SHAPE")
    t = f.readline().strip()
f.close()

f = open("pre-Q.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"Q-")
    t = f.readline().strip()
f.close()
f = open("pos-Q.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"-Q")
    t = f.readline().strip()
f.close()
f = open("adj.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"ADJ")
    t = f.readline().strip()
f.close()


f = open("keywords2.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"ATRIBUTEDSHAPE")
    t = f.readline().strip()
f.close()


f = open("relatedshape.txt",encoding='UTF-8')
t = f.readline().strip()
while(t!=""):
    keywordProcessor.add_keyword(t,"RELATEDSHAPE")
    t = f.readline().strip()
f.close()
print(keywordProcessor.get_all_keywords())
#open file and split words
f = open(input,encoding='UTF-8')
t = f.read()
task = t.split("^")
a=0
while a<len(task):
    r = 0
    key_found = keywordProcessor.extract_keywords(task[a].lower(),span_info=True)
    new_instance = keywordProcessor.replace_keywords(task[a].lower())
    new_instance = keywordProcessor.replace_keywords(new_instance)
    print(task[a])
    print(new_instance)
    a+=1
f.close()
