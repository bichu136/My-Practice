import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
def read_data(filename):
    r = []
    with open(filename) as file:
        line =file.readline() 
        while(line!=""):
            line= line.strip() +",1"
            print(line.split(','))
            k = 1
            for i in line.split(","):
                k = k*float(i)
            r.append([k,1])
            line = file.readline()
    return np.array(r,dtype=np.float64)
def read_data_y(filename):
    r = []
    with open(filename) as file:
        line =file.readline() 
        while(line!=""):
            # line+= ",1"
            line = line.strip()
            r.append([float(i) for i in line.split(",")])
            line = file.readline()
    return np.array(r,dtype=np.float64)
# Load the diabetes dataset

n = read_data('1.txt')
nlgn = np.transpose(np.vstack(((n[:,0])*np.log2(n[:,0]),n[:,1])))
lgn = np.transpose(np.vstack((np.log2(n[:,0]),n[:,1])))
nn = np.transpose(np.vstack(((n[:,0])*(n[:,0]),n[:,1])))
sqrt_n = np.transpose(np.vstack((np.sqrt(n[:,0]),n[:,1])))
y = read_data_y('2.txt')
def result(x,y,str):
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x, y)

    # Make predictions using the testing set
    y_pred = regr.predict(n)

    # The mean squared error
    print('Mean squared error of '+ str +': %.6f'
        % mean_squared_error(y, y_pred))
result(n,y,"$n$")
result(nlgn,y,"$nlog(n)$")
result(nn,y,"$n^2$")
result(lgn,y,"$log(n)$")
result(sqrt_n,y,"$\sqrt{n}$")
