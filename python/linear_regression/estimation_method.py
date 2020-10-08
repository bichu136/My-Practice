import numpy as np
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
inp = read_data('input.csv')
n = read_data('n.txt')
nlgn = read_data('nlogn.txt')
lgn = read_data('lgn.txt')
nn = read_data('nn.txt')
sqrt_n = read_data('sqrt_n.txt')
y = read_data_y('y.txt')

def model_prediction(x,y):
    r = np.dot(np.linalg.inv(np.dot(x.transpose(),x)),np.dot(x.transpose(),y))
    return r
def predict(x,model):
    return np.dot(x,model)
# r_input=  model_prediction(inp,y)
r_n = model_prediction(n,y)
r_nlgn = model_prediction(nlgn,y)
r_nn = model_prediction(nn,y)
r_sqrt_n = model_prediction(sqrt_n,y)
r_lg_n=model_prediction(lgn,y)
print(r_n,r_nlgn,r_nn,r_sqrt_n,r_lg_n,sep = '\n')
# y_input = predict(inp,r_input)
y_n=predict(n,r_n)
y_nlgn=predict(nlgn,r_nlgn)
y_nn=predict(nn,r_nn)
y_sqrt_n=predict(sqrt_n,r_sqrt_n)
y_lg_n=predict(lgn,r_lg_n)
# print(y_n,y_nlgn,y_nn,y_sqrt_n,sep = '\n')
# mean_input = ((y-y_input)**2).mean(axis=0)
mean_n=((y-y_n)**2).mean(axis=0)
mean_nlgn= ((y-y_nlgn)**2).mean(axis=0)
mean_nn= ((y-y_nn)**2).mean(axis=0)
mean_sqrt_n= ((y-y_sqrt_n)**2).mean(axis=0)
mean_sqrt_n= ((y-y_sqrt_n)**2).mean(axis=0)
print("min_MSE of O(n)",mean_n)
print("min_MSE of O(nlgn)",mean_nlgn)
print("min_MSE of O(nn)",mean_nn)
print("min_MSE of O(sqrt_n)",mean_sqrt_n)
print("min_MSE of O(lg_n)",mean_sqrt_n)