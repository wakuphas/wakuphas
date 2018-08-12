#!/usr/bin/env python
import numpy as np
#import cv
#import cv2
from PIL import Image
import pyfits
import matplotlib.pyplot as plt
from array import array
import scipy.optimize
from scipy import optimize
import math as math
import ROOT
from ROOT import *
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import ImageGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable


################
### colorbar ###
################
#p = 215   #[kBq/m^2]
p = 1682   #[kBq/m^2]
#L_air1 = 110 #[m]
L_air1 = 354 #[m]
#L_air1 = 136 #[m]
L_air2 = 69 #[m]


height, doserate = [],[]
data_x = np.loadtxt("662.dat", comments="#", delimiter=' ')


for i in range (0,len(data_x[:,0])):
    height.append(data_x[i,0])
    doserate.append(data_x[i,1])

y = np.arange(0.5, 160, 0.5)
x = np.arange(0, 60, 10)



X, Y = np.meshgrid(x, y)
Z1 = 2.4e-4 * np.log(np.power((L_air1/Y), 2) + 1.0) * p
Z2 = 2.4e-4 * np.log(np.power((L_air2/Y), 2) + 1.0) * p



##########
## fig ###
##########

fig = plt.figure(figsize=(4, 8))



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

#"""
ax1 = fig.add_subplot(1, 2, 1)
ax1.pcolormesh(X, Y, Z2, cmap='gist_ncar')
#plt.pcolor(X, Y, Z, cmap='hsv')
#ax1.set_xlabel('X', fontsize=24)
ax1.set_ylabel('Height [m]', fontsize=18)
ax1.set_xlabel('Theory', fontsize=18)
ax1.tick_params(labelbottom="off",bottom="off")


ax2 = fig.add_subplot(1, 2, 2)
ax2.pcolormesh(X, Y, Z1, cmap='gist_ncar')
ax2.set_xlabel('Observed', fontsize=18)
ax2.tick_params(labelbottom="off",bottom="off")


plt.subplots_adjust(wspace=0.5, hspace=0.3, bottom=0.2, left=0.2)
#"""





##
##
"""
fig, ax = plt.subplots()

image = ax.pcolormesh(X, Y, Z1, cmap='gist_ncar')
ax.axis("image")

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="10%", pad=1.0)
fig.add_axes(ax_cb)
plt.colorbar(image, cax=ax_cb, label=u'dose rate [\u03bcSv/h]')
"""
##
##


##
##
"""
# Set up figure and image grid

grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                 nrows_ncols=(1,2),
                 axes_pad=0.15,
                 share_all=True,
                 cbar_location="right",
                 cbar_mode="single",
                 cbar_size="7%",
                 cbar_pad=3
                )

# Add data to image grid

print(grid)
for ax in grid:
    im1 = ax.pcolormesh(Y, X, Z1, cmap='gist_ncar')
    im2 = ax.pcolormesh(X, Y, Z2, cmap='gist_ncar')


# Colorbar
ax.cax.colorbar(im1)
ax.cax.toggle_label(True)
ax.cax.set_label('HHH')
"""
##
##



######



plt.show()

# set path
pp = PdfPages('pdf.pdf')

# save figure
pp.savefig(fig)

# close file
pp.close()

####
"""
pp=plt.colorbar (orientation="vertical")
pp.set_label("Label", fontname="Arial", fontsize=24)

plt.xlabel('X', fontsize=24)
plt.ylabel('Y', fontsize=24)
"""




