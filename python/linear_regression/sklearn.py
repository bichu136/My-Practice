import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
def read_data(filename):
    r = []
    with open(filename) as file:
        line =file.readline() 
        while(line!=""):
            line+= ",1"
            r.append([float(i) for i in line.split(",")])
            line = file.readline()
    return np.array(r,dtype=np.float64)
def read_data_y(filename):
    r = []
    with open(filename) as file:
        line =file.readline() 
        while(line!=""):
            # line+= ",1"
            r.append([float(i) for i in line.split(",")])
            line = file.readline()
    return np.array(r,dtype=np.float64)
# Load the diabetes dataset
n = read_data('n.txt')
nlgn = np.transpose(np.vstack(((n[:,0])*np.log2(n[:,0]),n[:,1])))
lgn = np.transpose(np.vstack((np.log2(n[:,0]),n[:,1])))
nn = np.transpose(np.vstack(((n[:,0])*(n[:,0]),n[:,1])))
sqrt_n = np.transpose(np.vstack((np.sqrt(n[:,0]),n[:,1])))
y = read_data_y('time.txt')
def result(x,y,str):
    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(x, y)

    # Make predictions using the testing set
    y_pred = regr.predict(n)

    # The mean squared error
    print('Mean squared error of '+ str +': %.2f'
        % mean_squared_error(y, y_pred))
result(n,y,"n")
result(nlgn,y,"nlgn")
result(nn,y,"nn")
result(lgn,y,"lgn")
result(sqrt_n,y,"sqrt_n")
