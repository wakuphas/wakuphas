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
from ROOT import *
#from numpy import *



##############
### X axis ###
##############
X_mean, X_stack_mean = array('d'), array('d')
X_mean2, X_stack_mean2 = array('d'), array('d')
data_x = np.loadtxt("662_bkgv2.dat", comments="#", delimiter=' ')
data_x = np.loadtxt("662.dat", comments="#", delimiter=' ')

#data_x2 = np.loadtxt("geant662kev_Soildepth0.1cm.dat", comments="#", delimiter=' ')  # geant 4 soil=0.1cm


# Observed = Geant * hosei

for i in range (0,len(data_x[:,0])):
    X_mean.append(data_x[i,0])
    X_stack_mean.append(data_x[i,1])
    #X_mean2.append(data_x2[i,0])
    #X_stack_mean2.append(data_x2[i,2]) # geant 4

print "aho1"


#fit area
fit_min = 0.4
fit_max = 160


#log(h^-2+1)
#q[0]:p q[1]:L_air
def gauss(y, q):
    #result = 2.5e-4 * np.log(np.power(np.sqrt(q[1]*q[1]-y[0]*y[0]) /(y[0]), 2) + 1) * q[0]
    result = 2.5e-4 * np.log(np.power(q[1]/y[0], 2)+1) * q[0]
    return result
"""
#h^-1
def gauss(y, q):
    result = 2.2e-3 * q[0]/(y[0])
    return result
"""
ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")

print ""
print "fit min =",fit_min, "fit max =", fit_max
print "max X =", max(X_stack_mean)

parameter_optimal = array('d')
paramater_0 = 200
paramater_1 = 100



#diffuse
gau = ROOT.TF1("gauss", gauss, fit_min, fit_max, 2)
gau.SetParameters(paramater_0, paramater_1)
gau.SetParLimits(1,10.0,1000.0)
#gau.SetParLimits(1,68,70)
#gau.FixParameter(1,69.0)
#gau.FixParameter(1,29.0062)
#gau.FixParameter(2,2.32071)

gau.SetParNames("p [kBq]","L_air [m]")


# knot
"""
gau2 = ROOT.TF1("gauss2", gauss2, fit_min2, fit_max2, 3)
gau2.SetParameters(paramater_0, paramater_1, paramater_2)
gau2.FixParameter(0,38.5494)
gau2.FixParameter(1,29.0062)
gau2.FixParameter(2,2.32071)
"""
cv3 = ROOT.TCanvas("cs3", "Graph3", 20, 42, 600,600)
#cv3.SetLogx()
#cv3.SetLogy()
graph3 = ROOT.TGraph(len(X_mean), X_mean, X_stack_mean)
#graph3 = ROOT.TGraph(len(X_mean2), X_mean2, X_stack_mean2) # Geant 4

graph3.SetTitle("662keV fit")
graph3.SetMarkerStyle(1)
graph3.SetMarkerSize(1)
graph3.SetMarkerColor(ci)
graph3.SetFillColor(ci)
graph3.SetMarkerStyle(21)
graph3.SetMarkerSize(1.)
graph3.GetXaxis().SetTitle("Height [m]")
graph3.GetXaxis().CenterTitle()
graph3.GetYaxis().SetTitle("662 keV [#muSv/h]")
#graph3.GetYaxis().SetTitle("662 keV [cpm]")
graph3.GetYaxis().CenterTitle()
graph3.GetYaxis().SetTitleOffset(1.4)

#graph3.SetMinimum(1e-3)

graph3.Fit("gauss","R")
#graph3.Fit("gauss2","B")
#graph3.Fit("gauss2","Blue","same")
#gStyle.Set0ptFit();

graph3.Draw("APZ")


cv3.Update()


