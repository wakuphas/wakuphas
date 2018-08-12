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
from matplotlib.backends.backend_pdf import PdfPages


##############
# Parameters #
#############
MONTE_NUM = 1000
calc_NUM = 100

fit_min = 0.1 #cm
fit_max = 100 #cm

def func(y, q):
    result = q[0] * np.log(y[0]*q[1] + q[2]) + q[3]*y[0];
    #result = q[0] * np.log(y[0]*q[1] + q[2]) + q[3];
    return result
paramater_0 = 2.80058e+01
paramater_1 = 1.83659e+01
paramater_2 = 1.30348e+01
paramater_3 = -7.69248e-01


fig1 = plt.figure(figsize=(8,6))




################
# Loading data #
################
depth, L, Lerr = array('d'), array('d'), array('d')
data_1 = np.loadtxt("662.dat", comments="#", delimiter=' ')

for i in range (0,len(data_1[:,0])):
    depth.append(data_1[i,0])
    L.append(data_1[i,1])
    Lerr.append(data_1[i,2])

# real data plotting
plt.errorbar(depth,L,yerr=Lerr,fmt='ro',ecolor='r', ms=8, label="Geant 4") # observed


########################
# Creating random Lair #
########################
p0_list, p1_list, p2_list, p3_list = array('d'), array('d'), array('d'), array('d')
calc_list = [[] for i in range(calc_NUM)] # making empty list
calc_mean, calc_upper, calc_lower = array('d'),array('d'),array('d')

for s in range (0,MONTE_NUM):
    L_rand, Lerr_rand, color =array('d'), array('d'), array('d')
    for i in range (0,len(data_1[:,0])):
        #L_rand.append (np.random.normal()*Lerr[i] + L[i])
        L_rand.append (np.random.normal(L[i], Lerr[i], 1)) #


    ci = ROOT.TColor.GetColor("#99cccc")
    gau = ROOT.TF1("func", func, fit_min, fit_max, 4)
    gau.SetParameters(paramater_0, paramater_1, paramater_2, paramater_3)

    gau.SetParLimits(0,0,50)
    gau.SetParLimits(1,0,1000)
    gau.SetParLimits(2,0,50)
    gau.SetParLimits(3,-1,1)
    gau.FixParameter(3,0)

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
#   cv3.Update()
#    plt.plot(depth, L_rand, "o", color="black", ms=1)


    ################################
    # fitting lines wo kasane gaki #
    ################################
    x_calc = np.logspace(-1, 2, calc_NUM)
    calc = p0_list[s] * np.log(x_calc*p1_list[s] + p2_list[s]) + p3_list[s]*x_calc
#   plt.plot(x_calc, calc)

    ###################################################################
    # making calc_list[[calc[x0]],[calc[x1]], ... , [calc[calc_NUM]]] #
    ###################################################################
    for t in range (0,len(x_calc)):
        calc_list[t].append(p0_list[s] * np.log(x_calc[t]*p1_list[s] + p2_list[s]) + p3_list[s]*x_calc[t])
    """
    for t in range (0,len(x_calc)):
        code1 = 'calc_list{} = {}'.format(t, p0_list[s] * np.log(x_calc[t]*p1_list[s] + p2_list[s]) + p3_list[s]*x_calc[t])
        exec(code1)
    """
    s+=1


#print(calc_list)
for p in range (0,len(x_calc)):
    calc_mean.append(np.average(calc_list[p]))
    calc_upper.append(np.average(calc_list[p]) + np.std(calc_list[p]))
    calc_lower.append(np.average(calc_list[p]) - np.std(calc_list[p]))


#plt.plot(x_calc, calc_mean, ms=3, ls="--", color="r", label="Mean")
#plt.plot(x_calc, calc_upper, ms=3, ls="-", color="r", label="Fitting error")
#plt.plot(x_calc, calc_lower, ms=3, ls="-", color="r")
plt.fill_between(x_calc,calc_upper,calc_lower,facecolor='y',alpha=0.5, label="Fitting(Monte Carlo)")


##########################
# Plot best fit function #
##########################
"""
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

p0 = (mean_p0+sigma_p0)
q0 = (mean_p0-sigma_p0)
p1 = (mean_p1+sigma_p1)
q1 = (mean_p1-sigma_p1)
p2 = (mean_p2+sigma_p2)
q2 = (mean_p2-sigma_p2)
p3 = (mean_p3+sigma_p3)
q3 = (mean_p3-sigma_p3)

print "\n"
print "p0 = %.3f" % (mean_p0+sigma_p0)
print "q0 = %.3f" % (mean_p0-sigma_p0)
print "p1 = %.3f" % (mean_p1+sigma_p1)
print "q1 = %.3f" % (mean_p1-sigma_p1)
print "p2 = %.3f" % (mean_p2+sigma_p2)
print "q2 = %.3f" % (mean_p2-sigma_p2)
print "p3 = %.3f" % (mean_p3+sigma_p3)
print "q3 = %.3f" % (mean_p3-sigma_p3)


x = np.logspace(-1, 2)
y0 = mean_p0 * np.log(x*mean_p1 + mean_p2) + mean_p3*x # mean
y1 = p0 * np.log(x*p1 + p2) + p3*x # 1sigma
y2 = q0 * np.log(x*q1 + q2) + q3*x # 1sigma
plt.plot(x,y0, linestyle= "--" , color="r")
plt.plot(x,y1, "r")
plt.plot(x,y2, "r")
"""


# observed Lair
x = np.logspace(-1, 2)
y3 = 104 + x*0
y4 = 98  + x*0
y3 = 115 + x*0
y4 = 105  + x*0
plt.plot(x,y3, ls="--", c="b", label="Observed $L_{air}$")
plt.plot(x,y4, ls="--", c="b")



#np.random.seed()
#data = np.random.normal(72, 2.32/2, 10000)
#plt.hist(data, bins=100, normed=True)





############
# save fig #
############

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


#plt.xlabel("Depth distribution from the ground surface of $^{137}$Cs [cm]")
plt.xlabel(u'Buffer depth of $^{137}$Cs $\u03b2$ [cm]')
plt.ylabel("$L_{air}$ [m]")
plt.xscale("log")
#plt.legend(['G4 Data', 'Mean','Fitting error', '', 'Observed Lair'],loc="upper left")
plt.legend(loc="upper left")
"""
plt.plot(X_mean, X_stack_mean, 'o')
plt.plot(height, eps, '-')
plt.plot(height_app, eps_app, '-')
plt.legend(['Data','Theory', 'Approx.'])
plt.show()
"""
plt.show()

# set path
pp = PdfPages('pdf1.pdf')

# save figure
pp.savefig(fig1)

# close file
pp.close()



