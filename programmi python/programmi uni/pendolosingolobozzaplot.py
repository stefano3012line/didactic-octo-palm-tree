from scipy.sparse import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
import random
from scipy.stats import chisquare



t1 , theta1, t2, theta2 =np.loadtxt(r"/PENDOLOSINGOLO.txt", unpack=True)

omega2=4.5
phi2=4
A2=140
off=430
gamma2=0.1
p0=[omega2,phi2,gamma2,A2]
def sin(omega2,phi2, t2):
    return np.sin(omega2*t2+phi2)
plt.figure('Pendolo s')
theta2=theta2[:200]
t2=t2[:200]
plt.plot(t2,theta2)
plt.plot(t2,A2*sin(omega2,phi2,t2)+off)
plt.show()
ofs=np.mean(theta2)
sigma_theta2=10

def om(t , omega , phi0 , gamma ,A ):
    return A*np.exp(-gamma*t)*np.sin(phi0+omega*t)

popt,pcov= curve_fit(om, t2, theta2,p0=p0,absolute_sigma=True)
omega1,phi1,gamma1,A1=popt
print(popt)


fig=plt.figure('Pendolo singolo')
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.plot(t2, om(t2,omega1, phi1,gamma1,A1))
plt.grid(which='both',ls='dashed',color='gray')
plt.plot(t2[::1],theta2[::1]-ofs,'.')


fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 - om(t2,omega1, phi1,gamma1,A1)-ofs)/sigma_theta2
plt.errorbar(t2, res, sigma_theta2)
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)







plt.savefig('Pendolo singolo')

plt.show()
chiq=(np.sum((theta2-om(t2,omega1, phi1,gamma1,A1)-ofs)/sigma_theta2)**2)
print(chiq)
