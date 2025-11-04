import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


t1,theta1,t2,theta2=np.loadtxt(r"C:\Users\Dell\Desktop\Uni_lab\Dati oscillazioni accoppiate\BATTIMENTI.txt", unpack=True)
cunt=len(theta1)
#stima dei dati
p0=[160,160,0.03,0.04,5,5,5,5]
sigma_theta1=6
off=np.mean(theta1)
def om(t,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2):
    return A1*np.exp(-gamma1*t)*np.sin(omega1*t+phi1)+A2*np.exp(-gamma2*t)*np.sin(omega2*t+phi2)


popt,pcov=curve_fit(om,t1,theta1,p0=p0,absolute_sigma=True)
A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2=popt


#plot principale
fig=plt.figure('Battimenti1')
fig.add_axes((0.1, 0.37, 0.8, 0.6))
x=np.linspace(0,max(t1),10000)
plt.plot(x, om(x,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2),"g")
plt.plot(t1[::5],theta1[::5]-off,'.')
plt.errorbar(t1[::5],theta1[::5]-off,sigma_theta1,fmt='.')
plt.grid(which='both',ls='dashed',color='gray')

#stima degi errori
chiq=np.sum((((theta1-om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off))/sigma_theta1)**2)

print("chi^2=",chiq/cunt)

fig.add_axes((0.1, 0.1, 0.8, 0.2))
res = (theta1 - om(t1,A1,A2,gamma1,gamma2,phi1,phi2,omega1,omega2)-off)/sigma_theta1
plt.errorbar(t1[::15], res[::15], sigma_theta1,fmt=".")
plt.grid(which='both', ls='dashed', color='gray')
plt.xlabel('tempo')
plt.ylabel('posizione')
plt.ylim(-20.0, 20.0)

plt.savefig('Pendolo f')
plt.show()
