import json


waifu_in_stream = open("waifus.json",encoding="utf-8")
waifu_list = json.load(waifu_in_stream)

# remove all waifus that don't have bust waist and hip
i = 0
#
i = 0
while i<len(waifu_list):
    if (float(waifu_list[i]["bust"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
i = 0
print(len(waifu_list))
while i<len(waifu_list):
    if (float(waifu_list[i]["hip"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
i = 0
while i<len(waifu_list):
    if (float(waifu_list[i]["waist"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
while i<len(waifu_list):
    if (float(waifu_list[i]["height"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
while i<len(waifu_list):
    if (float(waifu_list[i]["weight"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
for waifu in waifu_list:
    print(str(waifu["trash"])+" "+str(waifu["likes"])+" "+waifu["name"]+" "+waifu["series"]["name"])
# file = open("log.txt",mode="w+",encoding="utf-8")
# file.write("origins:\n")
#
# for i in origin_dict.keys():
#     s=""
#     s+=i+"\n"
#     file.write(s)
# file.close()
# print(len(origin_dict))