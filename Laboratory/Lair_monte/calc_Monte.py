import numpy as np
from numpy.random import *
import pyfits
import math as math
#from RootPlot import RootPlot
import ROOT
from array import array
import sys
import subprocess
import os
from time import sleep
import matplotlib.pyplot as plt

##############
# Parameters #
##############
MONTE_NUM = 100

fit_min = 0.1 #cm
fit_max = 100 #cm

def func(y, q):
    result = q[0] * np.log(y[0]*q[1] + q[2]) + q[3]*y[0];
    return result
paramater_0 = 1
paramater_1 = 1
paramater_2 = 1
paramater_3 = 1

################
# Loading data #
################
depth, L, Lerr = array('d'), array('d'), array('d')
data_1 = np.loadtxt("662.dat", comments="#", delimiter=' ')

for i in range (0,len(data_1[:,0])):
    depth.append(data_1[i,0])
    L.append(data_1[i,1])
    Lerr.append(data_1[i,2])

########################
# Creating random Lair #
########################
p0_list, p1_list, p2_list, p3_list = array('d'), array('d'), array('d'), array('d')

for s in range (0,MONTE_NUM):
    L_rand, Lerr_rand, color =array('d'), array('d'), array('d')
    for i in range (0,len(data_1[:,0])):
        #L_rand.append (np.random.normal()*Lerr[i] + L[i])
        L_rand.append (np.random.normal(L[i], Lerr[i], 1)) #

    
    ci = ROOT.TColor.GetColor("#99cccc")
    gau = ROOT.TF1("func", func, fit_min, fit_max, 4)
    gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3)
    gau.SetParLimits(0,0,100)
    gau.SetParLimits(1,0,1000)
    gau.SetParLimits(2,-50,50)
    gau.SetParLimits(3,-10,10)
    #gau.SetParNames("p [kBq]","L_air [m]")
    graph3 = ROOT.TGraph(len(depth), depth, L_rand)
    graph3.Fit("func","R")
    """
    cv3 = ROOT.TCanvas("cs3", "Graph3", 20, 42, 600, 600)
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
    graph3.GetYaxis().CenterTitle()
    graph3.GetYaxis().SetTitleOffset(1.4)
    graph3.Draw("APZ")
    """
    p0_list.append(gau.GetParameter(0))
    p1_list.append(gau.GetParameter(1))
    p2_list.append(gau.GetParameter(2))
    p3_list.append(gau.GetParameter(3))
#    cv3.Update()

    plt.plot(depth, L_rand, "o", color="b")
    s+=1




mean_p0 = np.average(p0_list)
sigma_p0 = np.std(p0_list)
mean_p1 = np.average(p1_list)
sigma_p1 = np.std(p1_list)
mean_p2 = np.average(p2_list)
sigma_p2 = np.std(p2_list)
mean_p3 = np.average(p3_list)
sigma_p3 = np.std(p3_list)
print "\n**********\n"
print "fit min =",fit_min, "fit max =", fit_max
print "\n"

print "mean p0 = %.3f" % (mean_p0)
print "mean p1 = %.3f" % (mean_p1)
print "mean p2 = %.3f" % (mean_p2)
print "mean p3 = %.3f" % (mean_p3)

print "\n"
print "p0 = %.3f" % (mean_p0+sigma_p0)
print "q0 = %.3f" % (mean_p0-sigma_p0)
print "p1 = %.3f" % (mean_p1+sigma_p1)
print "q1 = %.3f" % (mean_p1-sigma_p1)
print "p2 = %.3f" % (mean_p2+sigma_p2)
print "q2 = %.3f" % (mean_p2-sigma_p2)
print "p3 = %.3f" % (mean_p3+sigma_p3)
print "q3 = %.3f" % (mean_p3-sigma_p3)


plt.xscale("log")
plt.show()


np.random.seed()
data = np.random.normal(72, 2.32/2, 10000)

plt.hist(data, bins=100, normed=True)

plt.show()


