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
from matplotlib.backends.backend_pdf import PdfPages




fig1 = plt.figure(figsize=(8,6))


#################
### plot data ###
#################
X_30, Y_30 = [],[]
data_x = np.loadtxt("30-100.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_30.append(data_x[i,0])
    Y_30.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="r")
print(X_30, Y_30)
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.538190402, 1.211012836, 1.397627155, 1.982949717, 2.174716078, 3.003116816, 3.769468938, 4.895359359, 5.222104833, 5.354163419, 6.494359285, 10.35934116], 'o', c="r")

X_100, Y_100 = [],[]
data_x = np.loadtxt("100-200.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_100.append(data_x[i,0])
    Y_100.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="b")
print(X_100, Y_100)
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.98862585000000003, 1.959276692, 2.0935040589999998, 2.799537264, 2.9815730020000002, 4.0162265980000003, 4.5136359529999996, 5.6686071919999996, 6.0803479280000001, 6.0976201769999996, 7.3703666170000002, 10.8714108], 's', c="m")


X_200, Y_200 = [],[]
data_x = np.loadtxt("200-300.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_200.append(data_x[i,0])
    Y_200.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="m")
print(X_200, Y_200)
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.80600486400000004, 1.4175845090000001, 1.470588749, 1.863260256, 1.9205221619999999, 2.4951172540000002, 2.7534868019999998, 3.360990138, 3.699633017, 3.5575475769999998, 4.3292441220000004, 6.3479710220000003], '^', c="y")

X_300, Y_300 = [],[]
data_x = np.loadtxt("300-400.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_300.append(data_x[i,0])
    Y_300.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="m")
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.75311895600000001, 1.176575962, 1.130903574, 1.528272461, 1.4991152190000001, 1.9903203570000001, 2.1106163449999999, 2.6477058429999998, 2.7071153429999999, 2.7674164889999999, 3.3236425719999998, 4.8676524060000004], '+', c="g")

X_400, Y_400 = [],[]
data_x = np.loadtxt("400-500.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_400.append(data_x[i,0])
    Y_400.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="m")
print(X_400, Y_400)
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.807727219, 1.114280827, 1.0840950300000001, 1.3711355510000001, 1.3531093869999999, 1.6987175080000001, 1.8102162420000001, 2.269405474, 2.4621103299999998, 2.3396309799999999, 2.8633759699999999, 3.8805619830000002], 'd', c="c")


X_500, Y_500 = [],[]
data_x = np.loadtxt("500-600.txt", comments="#", delimiter=' ')
for i in range (0,len(data_x[:,0])):
    X_500.append(data_x[i,0])
    Y_500.append(data_x[i,1])
#plt.plot(data_x[i,0],data_x[i,1], 'o', c="m")
print(X_500, Y_500)
plt.plot([0.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 150.0], [0.70837160600000004, 1.031749445, 0.91137530499999997, 1.2286528430000001, 1.163370182, 1.4064761189999999, 1.670490402, 2.0706608599999998, 1.991558398, 1.987802694, 2.4300839449999998, 3.3425019140000001], 'x', c="b")

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
params = {'backend': 'ps', #
    'axes.labelsize': 15, #
    'text.fontsize': 15, #
    'legend.fontsize': 15, #
    'xtick.labelsize': 15, #
    'ytick.labelsize': 15,
    'text.usetex': False} #
plt.rcParams.update(params)

plt.xlabel('Height [m]')
plt.ylabel('Ratio to 662 keV dose rate')
#plt.ylabel(u'${\epsilon}_{\mathrm{abs}}$ [$\mathrm{\mu}$Sv/h]  [\u03bcm]')



plt.legend(['30-100 keV', '100-200 keV', '200-300 keV', '300-400 keV', '400-500 keV', '500-600 keV'], loc='upper left')
#plt.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0, fontsize=18)
plt.show()



# set path
pp = PdfPages('pdf1.pdf')

# save figure
pp.savefig(fig1)

# close file
pp.close()


###################
###################

