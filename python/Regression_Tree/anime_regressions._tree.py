import csv
import pandas as pd
import numpy as np
import json
from regressiondecisiontreenode import Node
import sklearn.tree as tr

anime_raw= pd.read_csv("AnimeList.csv")

# make all NaN to 0.0
anime_preprocessed = anime_raw.fillna(0.0)
#remove 0.0 in studio
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["studio"]!=0.0]
#remove genre == 0.0
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["genre"]!=0.0]
# status Not yet aired
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["status"]!="Not yet aired"]
#select movie and TV
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["type"].isin(["Movie","TV"])]
#epsodes>0
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["episodes"]>0]
#score > 0.0
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["score"]>0.0]
# remove Unknown and Other Source
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["source"]!="Unknown"]
anime_preprocessed = anime_preprocessed.loc[anime_preprocessed["source"]!="Other"]


# choose the atribute to process
X_features = ["genre","studio","source"]
y_features = ["score","rank","popularity"]
# asign x and y
anime = anime_preprocessed[X_features+y_features]
anime_X = anime_preprocessed[X_features]
anime_y = anime_preprocessed[y_features[0]]
# one-hot encode and split genre and studio
# -------source--------
source_hot_encode = pd.get_dummies(anime_X.source,prefix="Source")
anime_X.drop(['source'], axis=1, inplace=True)
anime_X = pd.concat([anime_X,source_hot_encode],axis=1,sort=False)
# -------genre---------
genres=[]
for i in anime_X.genre:
    tokens = i.split(',')
    for token in tokens:
        if token.strip() not in genres:
            genres.append(token.strip())
genres.sort()
for genre in genres:
    encoding = [genre in i for i in anime_X.genre]
    anime_X["genre_"+genre] = encoding
anime_X.drop(['genre'], axis=1, inplace=True)

# ------studio------
studios = []
for i in anime_X.studio:
    tokens = i.split()
    for token in tokens:
        if token.strip() not in studios:
            studios.append(token.strip())
studios.sort()
for studio in studios:
    encoding = [studio in i for i in anime_X.studio]
    anime_X["studio_"+studio]=encoding
anime_X.drop(['studio'], axis=1, inplace=True)
# split data
total = anime_X.shape[0]
split_rate = 0.1

midpoint= total - round((total*split_rate))
anime_x_train = anime_X[:midpoint]
anime_x_validate = anime_X[midpoint:]
anime_y_train = anime_y[:midpoint]
anime_y_validate = anime_y[midpoint:]
# print(anime_x_train.columns)
# print(anime_y_train.std())
# print(anime_y_train.loc[anime_x_train["Source_Original"]==1].std())
# print(anime_y_train.loc[anime_x_train["Source_Original"]==1].shape)
#
#
#
# def create_regression_decision_tree(x_train,y_train):
#     root_nodes =Node(None)



model = tr.DecisionTreeRegressor()

model.fit(anime_x_train,anime_y_train)

# t = pd.concat([anime_x_validate,anime_y_validate],axis=1,sort=False)
# sample = t.sample()
# print(t.columns)
# sample_y = sample[y_features[0]]
# sample_x = sample.drop(columns=[y_features[0]])
predict =model.predict(anime_x_validate)

results = pd.DataFrame({'Original': anime_y_validate, 'Predictions':predict, 'difference': [abs(x1 - x2) for (x1, x2) in zip(anime_y_validate, predict)]})
print(results)

print(results["difference"].mean())
print(results["difference"].std())
mistakes = results[results.difference >0.5]
print(1-(len(mistakes.values)/len(predict)))

import tensorflow
tensorflow.__version__
from keras.models import Sequential
from keras.layers import Dense, Activation

modelnn = Sequential()
modelnn.add(Dense(1, input_dim=train_X.shape[1]))
modelnn.add(Dense(1))
modelnn.summary() #Print model Summary

# Compile model
modelnn.compile(loss= "mean_absolute_error" , optimizer="adam", metrics=["mean_absolute_error"])

modelnn.fit(anime_x_train,anime_y_train, epochs=10)

from sklearn.metrics import mean_absolute_error
pred= modelnn.predict(val_X)
score = np.sqrt(mean_absolute_error(val_y,pred))
print (score)


y_test_nn = modelnn.predict(anime_x_validate)


print(y_test_nn)

# Define model
modeldeux = Sequential()
modeldeux.add(Dense(16, input_dim=train_X.shape[1]))
modeldeux.add(Dense(8))
modeldeux.add(Dense(1))
modeldeux.summary() #Print model Summary


modeldeux.compile(loss= "mean_absolute_error" , optimizer="adam", metrics=["mean_absolute_error"])

# Fit Model
modeldeux.fit(train_X, train_y, epochs=10)

from sklearn.metrics import mean_absolute_error
pred= modeldeux.predict(val_X)
score = np.sqrt(mean_absolute_error(val_y,pred))
print (score)

#Prediction using Neural Network
y_test_deux = modeldeux.predict(val_X)

print(y_test_deux)
