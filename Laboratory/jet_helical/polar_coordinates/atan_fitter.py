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


pi = 180/math.pi
add = 0 #root no figure size wo bigger ni dekiru

# fitting area #
fit_min = 25
fit_max = 55
################

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
plt.xlabel("Distance from the core [arcsec]")
plt.ylabel("Position Angle [deg.]")
#plt.plot(r, theta, 'o')
plt.plot(r2, theta2, 'bo',)

fit_min = 25
fit_max = 55
q0 = 4
q1 = 15
q2 = 20
q3 = 1
q0 = 2.64
q1 = 15
q2 = -15
q3 = 1
q0 = -1.5
q1 = 5
q2 = 0.35
x = np.arange(fit_min, fit_max, 0.1)
#y = q0*np.sin((q1 * x + q2)/pi) +q3
y = q0 * np.arctan(q1 * np.sin(q2 * x))
plt.plot(x, y, "red")

plt.show()



###########
# fitting #
###########
"""
def sin(y, q):
    result = q[0] * math.sin((q[1] * y[0] + q[2])/pi) + q[3]
    return result
    """
"""
def sin(y, q):
    result = q[0] * math.sin((q[1] * y[0] + q[2])/pi) + q[3] + q[4] * math.sin((q[5] * y[0] + q[6])/pi)
    return result
"""
def sin(y, q):
    result = q[0]*math.atan(q[1]*math.sin((q[2] * y[0])))
    return result

ci = ROOT.TColor.GetColor("#99cccc")
ci2 = ROOT.TColor.GetColor("#000000")


print ""

parameter_optimal = array('d')
paramater_0 = 0.1
paramater_1 = 15
paramater_2 = 15
paramater_3 = 20
paramater_4 = 10
paramater_5 = 10
paramater_6 = 10
paramater_7 = 10

gau = ROOT.TF1("sin", sin, fit_min, fit_max, 3)
#gau.SetParameters(paramater_0, paramater_1, paramater_2)
gau.SetParameters(paramater_0, paramater_1, paramater_2)
#gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3, paramater_4, paramater_5, paramater_6)

gau.SetParLimits(0,-3,0)
gau.SetParLimits(1,2,10)
gau.SetParLimits(2,0,1)
#gau.SetParLimits(3,0,15)
#gau.SetParLimits(4,1,100)

gau.FixParameter(0,-1.5)
gau.FixParameter(1,5)
gau.FixParameter(2,0.35)
#gau.FixParameter(3,2)
#gau.FixParameter(4,34.)



    
    
cv3 = ROOT.TCanvas("cs3", "Graph3", fit_min, fit_max, 600,600)
#cv3.SetLogx()
#cv3.SetLogy()
graph3 = ROOT.TGraph(len(r2), r2, theta2)

graph3.GetXaxis().SetRange(0,350);
#graph3.GetXaxis().SetRange(100,350);  #hyouji hanni, tanni ha nazo
#graph3.GetYaxis().SetRange(0,10);

graph3.SetTitle("arctan(sin) fit")
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
graph3.Draw("APZ")

cv3.Update()
    
    
