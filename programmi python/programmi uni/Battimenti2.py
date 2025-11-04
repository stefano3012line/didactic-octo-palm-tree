import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\BATTIMENTI.txt", unpack=True)
cunt=len(theta1)
#plot principale
p0=[200,200,0.003,0.004,5,5,4.3,4.3]

off=np.mean(theta2)
def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)

sigma_theta1=6

popt,pcov=curve_fit(om,t2,theta2,p0=p0,absolute_sigma=True)
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt

fig=plt.figure('Battimenti2')
x=np.linspace(0,43,10000)
fig.add_axes((0.1, 0.37, 0.8, 0.6))
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2))
plt.errorbar(t2[::5],theta2[::5]-off,sigma_theta1,fmt='.')
#plt.plot(t2[::15],theta2[::15]-off,'.')
plt.grid(which='both',ls='dashed',color='gray')

#stima errori

chiq=np.sum((((theta2-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)**2)/sigma_theta1**2))
print("chi^2=",chiq/cunt)

#plot residui
fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta2 - om(t2,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)/sigma_theta1
plt.errorbar(t2[::15], res[::15], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)


plt.savefig('Pendolo f')
plt.show()