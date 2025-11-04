from scipy.sparse import random
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import math
import random
from scipy.stats import chisquare
#loading
t1 , theta1, t2, theta2 =np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\PENDOLOSMORZATO.txt", unpack=True)
cunt=len(theta1)
#plot del guess
omega1=4
phi1=5
A1=120
off=np.mean(theta1)
gamma1=1
p0=[omega1,phi1,gamma1,A1]
def sin(omega1,phi1, t1):
  return np.sin(omega1*t1+phi1)
plt.figure('Pendolo s')
plt.plot(t1,theta1,"b")
plt.plot(t1,A1*sin(omega1,phi1,t1)+off,"r")

#plot dell'pendolo


ofs=np.mean(theta1)
sigma_theta1=5

def om(t , omega , phi0 , gamma ,A ):
  return A*np.exp(-gamma*t)*np.sin(phi0+omega*t)

popt,pcov= curve_fit(om, t1, theta1,p0=p0,absolute_sigma=True)
omega1,phi1,gamma1,A1=popt


fig=plt.figure('Pendolo singolo')
fig.add_axes((0.1, 0.37, 0.8, 0.6))

t1=t1[200:]
theta1=theta1[200:]


x=np.linspace(10,41,10000)
plt.plot(x, om(x,omega1, phi1,gamma1,A1),color="r")
plt.grid(which='both',ls='dashed',color='gray')
plt.errorbar(t1[::10],theta1[::10]-ofs,sigma_theta1,fmt='.')
plt.plot(t1[::10],theta1[::10]-ofs,'.')


fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 - om(t1,omega1, phi1,gamma1,A1)-ofs)/sigma_theta1
plt.errorbar(t1[::15], res[::15], sigma_theta1,fmt=".")
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
chiq=np.sum((((theta1-om(t1,omega1, phi1,gamma1,A1)-ofs)**2)/sigma_theta1**2))
print("chi^2=",chiq/cunt)