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



##############
### X axis ###
##############
X_mean, X_stack_mean = array('d'), array('d')
data_x = np.loadtxt("test.txt", comments="#", delimiter=' ')
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
plt.show()


### root ###
#y,q = diffuse; Y,Q =knot
def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]
    return result

def gauss2(Y, Q):
    result = Q[0]*np.exp(-0.5*np.power((Y[0]-Q[1])/Q[2], 2))
    return result

ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")

#fit area
fit_min = 10
fit_max = 50
fit_min2 = 25
fit_max2 = 50


print ""
print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
print "max X_stack_mean =", max(X_stack_mean)

parameter_optimal = array('d')
paramater_0 = max(X_stack_mean)
paramater_1 = fit_min
paramater_2 = 10
paramater_3 = min(X_stack_mean)

paramater_4 = max(X_stack_mean)
paramater_5 = fit_min
paramater_6 = 10

#diffuse
gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 4)
gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3)
gau.SetParLimits(0,0,50.0)


# knot
gau2 = ROOT.TF1("gauss2", gauss2, fit_min2, fit_max2, 3)
gau2.SetParameters(paramater_0, paramater_1, paramater_2)
gau2.FixParameter(0,38.5494)
gau2.FixParameter(1,29.0062)
gau2.FixParameter(2,2.32071)

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
#graph3.Fit("gauss2","B")
graph3.Fit("gauss2","Blue","same")
graph3.Draw("APZ")

#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv3.Update()


