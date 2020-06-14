import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import requests
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from datetime import date,timedelta
import io

def log_curve(x,k,x_0,ymax):
    
    return ymax/(1+np.exp(-k*(x-x_0)))

def predict(xdata,ydata,data,country,day,fitted):
    print(xdata)
    #print(ydata)
    model = MLPRegressor(hidden_layer_sizes=[32,32,10],max_iter= 50000,activation='relu',solver='adam',alpha = 0.0005,random_state=26)
    x_data = np.arange(len(xdata)).reshape(-1,1)
    #y_data = np.arange(len(ydata
    _ = model.fit(x_data,ydata)
    test = np.arange(len(data) + 7).reshape(-1, 1)
    pred = model.predict(test)
    prediction = pred.round().astype(int)
    plt.plot(xdata, ydata, label="Confirmed", markersize=5.0)
    xdata = list(xdata) + list(range(len(xdata), len(xdata) + 7))

    plt.plot(xdata,prediction,marker='o',linestyle='None',markersize=3.0,label="Predicted")
    plt.legend(loc="upper left")
    newlabel = "Number of Days" + "\n\n" + "Gradual Slow after:" + str(int(fitted)) + "\n Peak Day: " + str(int(day))
    plt.xlabel(newlabel)
    plt.ylabel('Number of Cases')
    plt.title(country)
    plt.show()

def fitLogCurveByCountries(xdata,ydata):
    popt,pcov = curve_fit(log_curve,xdata,ydata)
    print("popt is")
    print(popt)
    estimated_k,estimated_x_0,ymax = popt
    print
    k = estimated_k
    x_0 = estimated_x_0
    y_fitted = log_curve(xdata,k,x_0,ymax)
    return x_0,ymax

def main():
    url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/key-countries-pivoted.csv"
    s = requests.get(url).content
    global_data = pd.read_csv("AttemptKaCSV.csv")
    print(global_data)
    global_data.head()
    country = "India"
    xdata = range(len(global_data.index))
    ydata = global_data[country]
    day,fitted = fitLogCurveByCountries(xdata,ydata)
    print("Day is "+str(day))
    test_1 = global_data[["Date",country]]
    print(test_1.shape)
    #test_1 = test_1.reshape(1, -1)
    #print(test_1.shape)
    predict(xdata, ydata, global_data[['Date', country]], country, day, fitted)


if __name__ == "__main__":
    main()
