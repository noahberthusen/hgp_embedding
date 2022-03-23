import matplotlib
import default_names
import numpy as np
import matplotlib.pyplot as plt
import argparse
import math
import scipy.stats
plt.style.use('seaborn-whitegrid')
#fig=plt.figure(figsize=(10, 8), dpi= 80, facecolor='w', edgecolor='k')
matplotlib.rcParams.update({'font.size': 20})
f, ax = plt.subplots(2, 2, sharex='col', sharey='row')

colors = ['red','blue','green','orange','yellow']
y = []
z = []

# With 6400

y.append(np.array([0.00386064895670557, 0.000237981999709036, 0.00013912080735112298, 5.311309104860662e-06, 3.7888489623494337e-07]))
y.append(np.array([0.024301979254334416, 0.0024518148114601734, 0.0011686327626667659, 9.839928301491607e-05, 1.0747572481650813e-05]))
y.append(np.array([0.0870957509250797, 0.010811667095701027, 0.005505485094408846, 0.000534194305840896, 9.124512350677794e-05]))
y.append(np.array([0.23567171264307185, 0.03810793739911578, 0.016108074662266714, 0.00279002683627505, 0.0004738928140617382]))
y.append(np.array([0.5019486538012312, 0.11852798183044111, 0.04714285714285715, 0.009061817746807477, 0.0020966747308002187]))
y.append(np.array([0.3454147263035029, 0.14556930570051185, 0.028530064152797907, 0.006774441878367954]))

x = np.array([400, 1600, 3600, 6400, 10000, 14400])

# Comment these lines if you want 6400
xa = np.delete(x,2)
ya = y.copy()
for i in range(5):
	ya[i] = np.delete(y[i],2)
	m = np.polyfit(xa**(1/4),ya[i],2)
	z.append(m[0]*(x**(1/2)) + m[1]*(x**(1/4)) + m[2])
	#z.append(m[0]*(x**(1/2)) + m[1])

ax[0,0].scatter(x,y[0],label="p = " + str(0.005),color=colors[0])
ax[0,0].plot(x,z[0],color=colors[0])
#ax[0,0].set(yscale='log')
ax[0,0].set(ylim=[-0.001,0.01])
ax[0,0].legend()

ax[0,1].scatter(x,y[1],label="p = " + str(2*0.005),color=colors[1])
ax[0,1].plot(x,z[1],color=colors[1])
#ax[0,1].set(yscale='log')
ax[0,1].legend()

ax[1,0].scatter(x,y[2],label="p = " + str(3*0.005),color=colors[2])
ax[1,0].plot(x,z[2],color=colors[2])
#ax[1,0].set(yscale='log')
ax[1,0].set(ylim=[-0.006,0.04])
ax[1,0].legend()

ax[1,1].scatter(x,y[3],label="p = " + str(4*0.005),color=colors[3])
ax[1,1].plot(x,z[3],color=colors[3])
#ax[1,1].set(yscale='log')
ax[1,1].legend()

plt.show()