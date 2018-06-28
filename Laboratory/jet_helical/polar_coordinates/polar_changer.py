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
plt.xlabel("Distance from the core [arcsec]")
#plt.xscale("log")
plt.ylabel("Position Angle [deg.]")
#plt.plot(r, theta, 'o')
plt.plot(r2, theta2, 'bo',)
plt.show()


