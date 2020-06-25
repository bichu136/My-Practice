import sys
import flashtext
input = sys.argv[1]
#create a Dictionary
f = open("keywords.txt",encoding='UTF-8')
MyDict= dict()
t = f.readline().strip()
keywordProcessor = flashtext.KeywordProcessor()
keywordProcessor.add_keywords_from_dict(MyDict)
while(t!=""):
    keywordProcessor.add_keyword(t)
    t = f.readline().strip()


print(keywordProcessor.get_all_keywords())
f.close()
#open file and split words
f = open(input,encoding='UTF-8')
t = f.read()
task = t.split("^")
a=0
while a<len(task):
    r = 0
    key_found = keywordProcessor.extract_keywords(task[a].lower(),span_info=True)
    print(key_found)
    print(task[a])
    for key,begin,end in key_found:
        print(task[a][begin:end+4])

    a+=1
f.close()
