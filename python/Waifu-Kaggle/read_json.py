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
i=0
while i<len(waifu_list):
    if (float(waifu_list[i]["height"])>0.0)==False:
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
i=0
while i<len(waifu_list):
    if (float(waifu_list[i]["weight"])<=0.0001):
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
i=0
while i<len(waifu_list):
    if (waifu_list[i]["blood_type"]==""):
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))
i=0
while i<len(waifu_list):
    waifu_list[i].==""):
        waifu_list.pop(i)
        i-=1
    i+=1
print(len(waifu_list))

for waifu in waifu_list:
    print(str(waifu["likes"])+" "+waifu["name"]+" "+waifu["series"]["name"])
# file = open("log.txt",mode="w+",encoding="utf-8")
# file.write("origins:\n")
#
# for i in origin_dict.keys():
#     s=""
#     s+=i+"\n"
#     file.write(s)
# file.close()
# print(len(origin_dict))


import tensorflow
print(tensorflow.__version__)
from keras.models import Sequential
from keras.layers import Dense, Activation

print(type(waifu_list))



# modelnn = Sequential()
# modelnn.add(Dense(1, input_dim=train_X.shape[1]))
# modelnn.add(Dense(1))
# modelnn.summary() #Print model Summary
#
# # Compile model
# modelnn.compile(loss= "mean_absolute_error" , optimizer="adam", metrics=["mean_absolute_error"])
#
# modelnn.fit(anime_x_train,anime_y_train, epochs=10)
#
# from sklearn.metrics import mean_absolute_error
# pred= modelnn.predict(val_X)
# score = np.sqrt(mean_absolute_error(val_y,pred))
# print (score)
#
#
# y_test_nn = modelnn.predict(anime_x_validate)
#
#
# print(y_test_nn)
#
# # Define model
# modeldeux = Sequential()
# modeldeux.add(Dense(16, input_dim=train_X.shape[1]))
# modeldeux.add(Dense(8))
# modeldeux.add(Dense(1))
# modeldeux.summary() #Print model Summary
#
#
# modeldeux.compile(loss= "mean_absolute_error" , optimizer="adam", metrics=["mean_absolute_error"])
#
# # Fit Model
# modeldeux.fit(train_X, train_y, epochs=10)
#
# from sklearn.metrics import mean_absolute_error
# pred= modeldeux.predict(val_X)
# score = np.sqrt(mean_absolute_error(val_y,pred))
# print (score)
#
# #Prediction using Neural Network
# y_test_deux = modeldeux.predict(val_X)
#
# print(y_test_deux)
