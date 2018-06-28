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

#fit area
fit_min = 42
fit_max = 53



##############
### X axis ###
##############
X_mean, X_stack_mean = array('d'), array('d')
data_x = np.loadtxt("projection.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_mean.append(data_x[i,0])
    X_stack_mean.append(data_x[i,1])


print "aho1"
#print X_mean
#print X_stack_mean



### python ###
def gauss(X_mean, A, B, C, D):
    return A*np.exp(-0.5*np.power((X_mean-B)/C, 2)) + D


parameter_optimal, covariance = optimize.curve_fit(gauss, X_mean, X_stack_mean, p0=[1,1,1,1],)
                                                   #bounds=([0,150,0,0],[1.e5,300,1.e5,1.e5]))
fitting = gauss(X_mean, parameter_optimal[0],parameter_optimal[1],parameter_optimal[2],parameter_optimal[3])

print "aho2"
plt.plot(X_mean, X_stack_mean, 'o')
plt.plot(X_mean, fitting)
#plt.show()


### root ###
#y,q = diffuse; Y,Q =knot
def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2))
    return result
"""
def gauss(y, q, Y, Q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]
    return result
"""
ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")



print ""
print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
print "max X_stack_mean =", max(X_stack_mean)

parameter_optimal = array('d')
paramater_0 = max(X_stack_mean)
paramater_1 = fit_min
paramater_2 = 10
#paramater_3 = min(X_stack_mean)


gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 3)
gau.SetParameters(paramater_0, paramater_1, paramater_2)



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


