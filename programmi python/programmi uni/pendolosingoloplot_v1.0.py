from scipy.sparse import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
import random
from scipy.stats import chisquare

t1 , theta1, t2, theta2 =np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\PENDOLOSINGOLO.txt", unpack=True)
cunt=len(theta2)

omega2=4.5
phi2=5
A2=100
off=430
gamma2=0.005
p0=[omega2,phi2,gamma2,A2]
def sin(omega2,phi2, t2):
  return np.sin(omega2*t2+phi2)

#plt.figure('Pendolo s')
#plt.plot(t2,theta2)
#plt.plot(t2,A2*sin(omega2,phi2,t2)+off)
#plt.show()
ofs=np.mean(theta2)
sigma_theta2=3

def om(t , omega , phi0 , gamma ,A ):
  return A*np.exp(-gamma*t)*np.sin(phi0+omega*t)

popt,pcov= curve_fit(om, t2, theta2,p0=p0,absolute_sigma=True)
omega1,phi1,gamma1,A1=popt
#print(popt)

fig=plt.figure('Pendolo singolo')
fig.add_axes((0.1, 0.37, 0.8, 0.6))

t2=t2[200:400]
theta2=theta2[200:400]


x=np.linspace(10,20.3,10000)
plt.plot(x, om(x,omega1, phi1,gamma1,A1))
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(t2[::],theta2[::]-ofs,sigma_theta2,fmt='.')
plt.plot(t2[::],theta2[::]-ofs,'.')

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 - om(t2,omega1, phi1,gamma1,A1)-ofs)/sigma_theta2
plt.errorbar(t2[::], res[::], sigma_theta2,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)

plt.savefig('Pendolo singolo')
plt.show()
print("omega1=",omega1)
print("phi1=",phi1)
print("gamma1=",gamma1)
print("A1=",A1)
print("tau=",1/gamma1)
chiq=np.sum((((theta2-om(t2,omega1, phi1,gamma1,A1)-ofs)**2)/sigma_theta2**2))
print("chi^2=",chiq/(cunt-4),'sigma_chi^2=',np.sqrt(2/(cunt-4)))
