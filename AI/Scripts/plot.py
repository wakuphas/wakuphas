#import Tkinter
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from array import array
from matplotlib import pylab as plt
import pylab



data = np.loadtxt("epochavg.txt",comments="#",delimiter=' ')

epoch, avg, Q_his = array('d'),array('d'),array('d')
#print data


for i in range (0,len(data[:,0])):
    epoch.append(data[i,0])
    avg.append(data[i,1])

#print(epoch)


#plt.ylim(0.5e-7,2.5e-7)
#plt.yscale("log")

plt.xlabel('Epoch')
plt.ylabel('avg')
plt.grid(True)
plt.plot(epoch, avg, "o-")
plt.show()






