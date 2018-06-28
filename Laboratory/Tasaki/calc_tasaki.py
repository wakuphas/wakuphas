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



####################
### calc eps_abs ###
####################
MAX = 150 #[m]
INF = 10000
bin = 1000.0

# constants
L_air = 101.0 #[m]
#L_air = 69.2 #[m]

mu = np.log(2)/L_air  #mu = 1.00e-2 #air [/m]
ita = 0.85 #Cs137
hw = 0.662 #[MeV]
zeta = 0.0327 #[cm^2/g] water
hw_zeta = hw*1.0e6*1.602e-19 * zeta*0.1 #= 3.5e-16[Sv m^2]

# Intensity
p = 221.0   #[kBq/m^2]




########################
# Calculation (Theory) #
########################
eps, height = array('d'), array('d')
for h in range (1,MAX+1):  #1m -150m
    f_muh = 0.0
    for s in range (0,INF):
        ss = 0.0
        ss = s/bin
        #print ss
        f_muh += 0.5*(ss*np.exp(-np.sqrt(ss*ss + (mu*h)*(mu*h)))) / (ss*ss + (mu*h)*(mu*h)) * (1.0/bin)
        if (h == 1):
            f_muh_1m = f_muh

    eps.append( hw_zeta * f_muh * ita * p * 3600 * 1.0e6 * 1.0e3 ) #Sv/s, Bq => micro Sv/h, kBq
    height.append(h)
    #print h, "[m], ", f_muh, eps[h]


f1 = open('epsilon.dat', 'w')
for h in range (0,MAX): #[0]=1m ,[149]=150m
    string1 = "%.3f %e\n" % ((height[h]), (eps[h]))
    f1.write(string1)
f1.close()



###############################
# Calculation (approximation) #
###############################
eps_app,eps_app1, height_app, relative_err = array('d'), array('d'), array('d'), array('d')
for h in range (1,MAX+1):
    eps_app.append( 2.5e-4 * np.log(np.power((L_air/h), 2) + 1.0) * p )
    height_app.append(h)
    relative_err.append((eps[h-1] - eps_app[h-1])/eps[h-1]*100)


"""
for i in range(0,MAX):
    print eps_app[i]
"""

print "\n************"
print "f_muh (h=1m) = ", f_muh_1m
print "eps_abs (h=1m) = ", eps[0], eps_app[0]
print "Intensity p = ", p, "[kBq]"



##################################
# relative_err (Theory vs. App.) #
##################################
print "\nrelative err"
print "1 m : %.2f" % ((eps[0] - eps_app[0])/eps[0]*100), "%"
height_list = np.arange(MAX)
for n in height_list:
    if n % 10 != 9:
        continue
    print n+1, "m: %.2f" % ((eps[n] - eps_app[n])/eps[n]*100), "%"



#################
### plot data ###
#################
X_mean, X_stack_mean = array('d'), array('d')
data_x = np.loadtxt("662.dat", comments="#", delimiter=' ')

for i in range (0,len(data_x[:,0])):
    X_mean.append(data_x[i,0])
    X_stack_mean.append(data_x[i,1])


"""
chi_squre1 = np.power(eps[1] - X_stack_mean[0], 2) / eps[1]
chi_squre10 = np.power(eps[10] - X_stack_mean[1], 2) / eps[10]
chi_squre20 = np.power(eps[20] - X_stack_mean[2], 2) / eps[20]
chi_squre30 = np.power(eps[30] - X_stack_mean[3], 2) / eps[30]
chi_squre40 = np.power(eps[40] - X_stack_mean[4], 2) / eps[40]
chi_squre50 = np.power(eps[50] - X_stack_mean[5], 2) / eps[50]
chi_squre60 = np.power(eps[60] - X_stack_mean[6], 2) / eps[60]
chi_squre70 = np.power(eps[70] - X_stack_mean[7], 2) / eps[70]
chi_squre80 = np.power(eps[80] - X_stack_mean[8], 2) / eps[80]
chi_squre90 = np.power(eps[90] - X_stack_mean[9], 2) / eps[90]
chi_squre100 = np.power(eps[100] - X_stack_mean[10], 2) / eps[100]
chi_squre150 = np.power(eps[150] - X_stack_mean[11], 2) / eps[150]


chi_squre = chi_squre1 + chi_squre10 + chi_squre20 + chi_squre30 + chi_squre40 + chi_squre50 + chi_squre60+ chi_squre70 + chi_squre80 + chi_squre90 + chi_squre100 + chi_squre150

print "chi_squre (Theory) =" , chi_squre
"""






fig1 = plt.figure(figsize=(8,6))

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
plt.ylabel(u'${\epsilon}_{\mathrm{abs}}$ [\u03bcSv/h]')
#plt.ylabel(u'${\epsilon}_{\mathrm{abs}}$ [$\mathrm{\mu}$Sv/h]  [\u03bcm]')


plt.plot(X_mean, X_stack_mean, 'o')
plt.plot(height, eps, '-')
plt.plot(height_app, eps_app, '-')
plt.legend(['Data','Theory', 'Approx.'])
plt.show()


# set path
pp = PdfPages('pdf1.pdf')

# save figure
pp.savefig(fig1)

# close file
pp.close()


###################
###################

fig2 = plt.figure(figsize=(8,6))

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
plt.ylabel('Relative Error [%]')

plt.ylim([-2,20])
plt.plot(height, relative_err, '-')
plt.legend(['Approx. vs. Theory'])
plt.show()

# set path
pp = PdfPages('pdf2.pdf')

# save figure
pp.savefig(fig2)

# close file
pp.close()


