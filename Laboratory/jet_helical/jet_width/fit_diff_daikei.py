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



### root ###
#y,q = diffuse; Y,Q =knot

#fit area
fit_min = 0
fit_max = 40





#gauss
"""
def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]   + q[4]*np.exp(-0.5*np.power((y[0]-q[5])/q[6], 2))
    return result



def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]   + (q[4]-q[5])/(1+np.power(q[6]/(y[0]-q[7]),q[8]))
    return result
"""

def gauss(y, q):
    result = (q[0]-q[1])/(1 + np.power(q[2]/(y[0]-q[3]), q[4]))
    return result


ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")



print ""
print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
print "max X_stack_mean =", max(X_stack_mean)


parameter_optimal = array('d')
paramater_0 = 0.1
paramater_1 = 15
paramater_2 = 15
paramater_3 = 20
paramater_4 = 10
paramater_5 = fit_min
paramater_6 = 10


"""
#diffuse
gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 7)
gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3, paramater_4, paramater_5, paramater_6)
gau.SetParLimits(0,0,50.0)
#gau.FixParameter(0,38.5494)
#gau.FixParameter(1,29.0062)
#gau.FixParameter(2,2.32071)

"""
# daikei
gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 5)
gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3, paramater_4)

gau.SetParLimits(0,1,50)
gau.SetParLimits(1,1,50)
gau.SetParLimits(2,10,40)
gau.SetParLimits(3,10,40)
gau.SetParLimits(4,1,100)

gau.FixParameter(0,0.1)

gau.FixParameter(1,6.)
gau.FixParameter(2,26.0)
gau.FixParameter(3,15.0)
gau.FixParameter(4,34.)
"""


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
#graph3.Fit("gauss2","Blue","same")
graph3.Draw("APZ")

#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv3.Update()


