#!/usr/bin/env python
import numpy as np
import cv 
import cv2
from PIL import Image

import pyfits
import matplotlib.pyplot as plt

from array import array

import scipy.optimize

from scipy import optimize
import math as math
import ROOT
#from numpy import *

add = 1 #root no figure size wo bigger ni dekiru


fit_min_x = 470
fit_max_x = 476

fit_min_y = 573
fit_max_y = 580



print "fit width ", fit_max_x - fit_min_x
print "fit height ", fit_max_y - fit_min_y

hdulist=pyfits.open('2015.fits')
hdu=hdulist[0]
data=hdu.data
header=hdu.header
height, width = data.shape
print "width=",width,"height=",height
#print data[height-1][width-1]


#print(data.shape, data.dtype)
print(data)
plt.imshow(data)
plt.show()



"""subete kakidasu
f1 = open('test.txt','w')
for y in range(0,height-1):
    for x in range(0,width-1):
        str1 = "%.7e " % data[y][x]
        f1.write(str1)
    str = "\n"
    f1.write(str)
f1.close()
"""
###

#only ROI is written
f1 = open('test.txt','w')
for y in range(fit_min_y-add,fit_max_y  + add):
    for x in range(fit_min_x-add,fit_max_x  + add):
        str1 = "%.7e " % data[y][x]
        f1.write(str1)
    str = "\n"
    f1.write(str)
f1.close()

print "width + %d*2 = " % add, fit_max_x - fit_min_x + add*2
print "height + %d*2 = " % add, fit_max_y - fit_min_y + add*2
f_root = open('width_height_for_root.txt','w')
str_x = "%d " % (fit_max_x - fit_min_x + add*2)
str_y = "%d " % (fit_max_y - fit_min_y + add*2)
str_minmax = "%d %d %d %d" % (fit_min_x-add, fit_max_x+add, fit_min_y-add, fit_max_y+add)

f_root.write(str_x)
f_root.write(str_y)
f_root.write(str_minmax)
f_root.close()
###




#AB = 0
#print AB

x_stack = array('d')
f2 = open('1d_profile_x.txt','w')
#for x in range(0,width-1):
for x in range(fit_min_x,fit_max_x):
    x_stack = 0
    for y in range(fit_min_y,fit_max_y):
        x_stack = x_stack + data[y][x]
    str2_1 = "%d " % x
    str2_2 = "%.7e" % x_stack
    f2.write(str2_1)
    f2.write(str2_2)
    f2.write(str)
f2.close()



y_stack = array('d')
f3 = open('1d_profile_y.txt','w')
#for y in range(0,height-1):
for y in range(fit_min_y,fit_max_y):
    y_stack = 0
    for x in range(fit_min_x,fit_max_x):
        y_stack = y_stack + data[y][x]
    str3_1 = "%d " % y
    str3_2 = "%.7e" % y_stack
    f3.write(str3_1)
    f3.write(str3_2)
    f3.write(str)
f3.close()







##############
### X axis ###
##############
x_root, x_stack2, X_mean, X_stack_mean = array('d'), array('d'), array('d'), array('d')
data_x = np.loadtxt("1d_profile_x.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    x_root.append(data_x[i,0])
    x_stack2.append(data_x[i,1])

"""
for i in range (0,len(data_x[:,0])):
    print x_stack2[i]
    print x_root[i]
"""


#print x_stack2[2]
"""
n = -1
t = -1 # bin number
for i in range (0,len(data_x[:,0])-1):
    if (x_stack2[i] == x_stack2[i+1]):
        n += 1
    else:
        t += 1
        #print "n,t=%d,%d" % (n, t)
        X_mean.append((x_root[i-n] + x_root[i])/2.)
        X_stack_mean.append(x_stack2[i])
        n = -1
"""
#print X_mean
#print X_stack_mean


X_mean = x_root
X_stack_mean = x_stack2

### python ###
def gauss(X_mean, A, B, C, D):
    return A*np.exp(-0.5*np.power((X_mean-B)/C, 2)) + D


parameter_optimal, covariance = optimize.curve_fit(gauss, X_mean, X_stack_mean, p0=[1000,100,100,1],)
                                                   #bounds=([0,150,0,0],[1.e5,300,1.e5,1.e5]))
fitting = gauss(X_mean, parameter_optimal[0],parameter_optimal[1],parameter_optimal[2],parameter_optimal[3])


plt.plot(X_mean, X_stack_mean, 'o')
plt.plot(X_mean, fitting)
plt.show()


### root ###

def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]
    return result


ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")

#fit area
fit_min = fit_min_x
fit_max = fit_max_x
print ""
print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
print "max X_stack_mean =", max(X_stack_mean)

parameter_optimal = array('d')
paramater_0 = max(X_stack_mean)
paramater_1 = fit_min_x
paramater_2 = 10
paramater_3 = min(X_stack_mean)

gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 4)
gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3)



cv3 = ROOT.TCanvas("cs3", "Graph3", 20, 42, 600,600)
#cv3.SetLogx()
#cv3.SetLogy()
graph3 = ROOT.TGraph(len(X_mean), X_mean, X_stack_mean)

graph3.SetTitle("Gauss fit")
graph3.SetMarkerStyle(1)
graph3.SetMarkerSize(1)
graph3.SetMarkerColor(ci)
graph3.SetFillColor(ci)
graph3.SetMarkerStyle(21)
graph3.SetMarkerSize(1.)
graph3.GetXaxis().SetTitle("X_mean")
graph3.GetXaxis().CenterTitle()
graph3.GetYaxis().SetTitle("Counts")
graph3.GetYaxis().CenterTitle()
#graph3.SetMinimum(1e-3)

graph3.Fit("gauss","R")
graph3.Draw("APZ")
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv3.Update()









##############
### Y axis ###
##############
y_root, y_stack2, Y_mean, Y_stack_mean = array('d'), array('d'), array('d'), array('d')
data_y = np.loadtxt("1d_profile_y.txt", comments="#", delimiter=' ')
for i in range (0,len(data_y[:,0])):
    Y_mean.append(data_y[i,0])
    Y_stack_mean.append(data_y[i,1])





### python ###
def gauss(Y_mean, A, B, C, D):
    return A*np.exp(-0.5*np.power((Y_mean-B)/C, 2)) + D


parameter_optimal, covariance = optimize.curve_fit(gauss, Y_mean, Y_stack_mean, p0=[1000,100,100,1])
fitting = gauss(Y_mean, parameter_optimal[0],parameter_optimal[1],parameter_optimal[2],parameter_optimal[3])


plt.plot(Y_mean, Y_stack_mean, 'o')
plt.plot(Y_mean, fitting)
plt.show()


### root ###

def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]
    return result


ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")

#fit area
#fit_min = min(Y_mean)
fit_min = fit_min_y
#fit_max = max(Y_mean)
fit_max = fit_max_y
print ""
print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
print "max Y_stack_mean =", max(Y_stack_mean)

parameter_optimal = array('d')
paramater_0 = max(Y_stack_mean)
paramater_1 = fit_min_y
paramater_2 = 10
paramater_3 = min(Y_stack_mean)


gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 4)
gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3)
#pow.SetLineColor(ci)

#lin = ROOT.TF1("lin", linear, -2, 2, 2)
#lin.SetParameters(2, -2.5)


cv3 = ROOT.TCanvas("cs3", "Graph3", 20, 42, 600,600)
#cv3.SetLogx()
#cv3.SetLogy()
graph3 = ROOT.TGraph(len(Y_mean), Y_mean, Y_stack_mean)

graph3.SetTitle("Gauss fit")
graph3.SetMarkerStyle(1)
graph3.SetMarkerSize(1)
graph3.SetMarkerColor(ci)
graph3.SetFillColor(ci)
graph3.SetMarkerStyle(21)
graph3.SetMarkerSize(1.)
graph3.GetXaxis().SetTitle("Y_mean")
graph3.GetXaxis().CenterTitle()
graph3.GetYaxis().SetTitle("Counts")
graph3.GetYaxis().CenterTitle()
#graph3.SetMinimum(1e-3)

graph3.Fit("gauss","R")
graph3.Draw("APZ")
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv3.Update()

#python -i fits_scanner.py de tomattekureru



