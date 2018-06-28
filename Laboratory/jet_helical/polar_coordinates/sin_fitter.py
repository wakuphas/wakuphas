#!/usr/bin/env python
# coding:utf-8
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

add = 0 #root no figure size wo bigger ni dekiru


fit_min_x = 0
fit_max_x = 804

fit_min_y = 481
fit_max_y = 1023

core_x = 804
core_y = 481
#core_x = 675
#core_y = 475

arcsec = 0.5 # arcsec/pixel

print "fit width ", fit_max_x - fit_min_x
print "fit height ", fit_max_y - fit_min_y

hdulist=pyfits.open('2005-2009.fits')
hdu=hdulist[0]
data=hdu.data
header=hdu.header
height, width = data.shape
print "width=",width,"height=",height
#print data[height-1][width-1]

#ax = plt.gca()
#ax.invert_yaxis()
print(data)
##plt.imshow(data)
##plt.ylim(plt.ylim()[::-1])
##plt.show()



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


r, theta, data_rtheta  = array('d'), array('d'), array('d')
for y in range(fit_min_y,fit_max_y):
    for x in range(fit_min_x,fit_max_x):
        if (data[y][x] >= 5 and data[y][x] < 15  and x<=core_x and y>=core_y):
            r.append((pow((x-core_x)*(x-core_x) + (y-core_y)*(y-core_y), 0.5)) * arcsec)
            theta.append(90-math.atan2(y-core_y,core_x-x)*180/math.pi-54)
            data_rtheta.append(data[y][x])

r2, theta2, data_rtheta2  = array('d'), array('d'), array('d')
for y in range(fit_min_y,fit_max_y):
    for x in range(fit_min_x,fit_max_x):
        if (data[y][x] >= 15 and x<=core_x and y>=core_y):
            r2.append((pow((x-core_x)*(x-core_x) + (y-core_y)*(y-core_y), 0.5)) * arcsec)
            theta2.append(90-math.atan2(y-core_y,core_x-x)*180/math.pi-54)
            data_rtheta2.append(data[y][x])



print "core center's counts = %d" % data[core_y][core_x]
print "success!!"

#plt.title("title")
#plt.xlabel("Distance from the core [arcsec]")
#plt.ylabel("Position Angle [deg.]")
#plt.plot(r, theta, 'o')
#plt.plot(r2, theta2, 'bo',)
#plt.show()



###########
# fitting #
###########
"""
    def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]   + q[4]*np.exp(-0.5*np.power((y[0]-q[5])/q[6], 2))
    return result
    
    
    
    def gauss(y, q):
    result = q[0]*np.exp(-0.5*np.power((y[0]-q[1])/q[2], 2)) + q[3]   + (q[4]-q[5])/(1+np.power(q[6]/(y[0]-q[7]),q[8]))
    return result
    """

pi = 180/math.pi
def sin(y, q):
    result = q[0] * math.sin(q[1]*y[0]/pi)+(q[2]/pi)
    return result


ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")


fit_min = 25
fit_max = 60
print ""
#print "fit min =",fit_min, "Hz, fit max =", fit_max, "Hz"
#print "max X_stack_mean =", max(X_stack_mean)


parameter_optimal = array('d')
paramater_0 = 0.1
paramater_1 = 15
paramater_2 = 15
paramater_3 = 20
paramater_4 = 10

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
gau = ROOT.TF1("sin", sin, fit_min, fit_max, 3)
gau.SetParameters(paramater_0, paramater_1, paramater_2)

gau.SetParLimits(0,0,50)
#gau.SetParLimits(1,1,50)

#gau.SetParLimits(2,10,40)
#gau.SetParLimits(3,10,40)
#gau.SetParLimits(4,1,100)

#gau.FixParameter(0,0.1)
#gau.FixParameter(1,6.)
#gau.FixParameter(2,26.0)
#gau.FixParameter(3,15.0)
#gau.FixParameter(4,34.)



    
    
cv3 = ROOT.TCanvas("cs3", "Graph3", 20, 42, 600,600)
#cv3.SetLogx()
#cv3.SetLogy()
graph3 = ROOT.TGraph(len(r2), r2, theta2)

graph3.GetXaxis().SetRange(100,350);
graph3.GetYaxis().SetRange(0,10);

graph3.SetTitle("Sin fit")
graph3.SetMarkerStyle(1)
graph3.SetMarkerSize(1)
graph3.SetMarkerColor(ci)
graph3.SetFillColor(ci)
graph3.SetMarkerStyle(21)
graph3.SetMarkerSize(1.)
graph3.GetXaxis().SetTitle("r")
graph3.GetXaxis().CenterTitle()
graph3.GetYaxis().SetTitle("P.A.")
graph3.GetYaxis().CenterTitle()
#graph3.SetMinimum(1e-3)
    
graph3.Fit("sin","R")
#graph3.Fit("gauss2","B")
#graph3.Fit("gauss2","Blue","same")
graph3.Draw("APZ")
    
#cv2.waitKey(0)
#cv2.destroyAllWindows()
cv3.Update()
    
    
